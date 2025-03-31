from flask import Blueprint, request, jsonify,render_template,send_file
from datetime import datetime,timezone
from models import db, User, Course, Subject, Chapter,Question,Option,QuizResult  # Added models for new endpoints
import sqlite3
from flask import Flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager,get_jwt
from flask_cors import cross_origin
import csv
import io
from flask import current_app as app
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Use a strong secret key
jwt = JWTManager(app)
routes = Blueprint('routes', __name__)



ADMIN_USERNAME = "Ujju"
ADMIN_PASSWORD = "985679"

def valid_user(username, course):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND course = ?', 
                        (username, course)).fetchone()
    conn.close()
    return user is not None

@routes.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json

    # Extract username and password from request data
    username = data.get('username')
    password = data.get('password')

    # Check if credentials match hardcoded values
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({'success': True, 'redirect_url': '/admin-dashboard'})
    else:
        return jsonify({'success': False, 'error': 'Invalid admin credentials'})
    
@routes.route('/admin-dashboard')
def admin_dashboard():
    return render_template('index.html')



# -------------------- LOGIN FUNCTIONALITY -------------------- #

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

from flask import jsonify, request
from flask_jwt_extended import create_access_token

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    user = conn.execute('SELECT * FROM user WHERE username = ? AND password = ?', 
                        (username, password)).fetchone()
    conn.close()

    if user:
        identity_data = f"{username}:{user['course']}"  # 🔥 Encode as string
        access_token = create_access_token(identity=identity_data)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    identity = get_jwt_identity()  # Now in format "username:course"
    print("🔐 Protected Route - Token Data:", identity)

    try:
        username, course = identity.split(':')  # 🔥 Extract values from string
    except ValueError:
        return jsonify({"error": "Invalid token format"}), 400

    return jsonify({
        "username": username,
        "course": course
    }), 200

@routes.route('/subjects1', methods=['GET'])
@jwt_required()
def get_subjects1():
    identity = get_jwt_identity()  # Now in format "username:course"
    print("🔎 Token Data (identity):", identity)

    try:
        username, course = identity.split(':')  # 🔥 Extract values from string
    except ValueError:
        return jsonify({"error": "Invalid token format"}), 400

    conn = get_db()
    subjects = conn.execute(
        'SELECT s.id AS subject_id , s.name FROM subject s JOIN course c ON s.course_id = c.id WHERE c.name = ?;', 
        (course,)
    ).fetchall()
    conn.close()

    return jsonify([{"subject_id": subject['subject_id'], "name": subject['name']} for subject in subjects])

@routes.route('/chapters1/<subject_id>', methods=['GET'])
@jwt_required()
def get_chapters1(subject_id):
    print("✅ Received subject_id:", subject_id)  # Debug log

    identity = get_jwt_identity()  
    print("🔎 Token Data (Chapters Route):", identity)

    try:
        username, course = identity.split(':')
    except ValueError:
        return jsonify({"error": "Invalid token format"}), 400

    conn = get_db()
    chapters = conn.execute('SELECT id, name FROM chapter WHERE subject_id = ?', (subject_id,)).fetchall()
    conn.close()

    return jsonify([{"id": chapter['id'], "name": chapter['name']} for chapter in chapters])


@routes.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Extracting data from the request
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    dob = data.get('dob')  # Date of Birth
    gender = data.get('gender')
    course = data.get('course')

    # Check if required fields are missing
    if not all([username, password, email, dob, gender, course]):
        return jsonify({'success': False, 'error': 'All fields are required.'}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'error': 'Username already exists.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'error': 'Email already exists.'}), 400

    # Convert DOB to the proper date format
    try:
        dob = datetime.strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Create a new user instance
    new_user = User(
        username=username,
        password=password,
        email=email,
        dob=dob,
        gender=gender,
        course=course
    )

    # Add user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User registered successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500




# -------------------- COURSE FUNCTIONALITY -------------------- #

@routes.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': course.id, 'name': course.name} for course in courses])

@routes.route('/add-course', methods=['POST'])
def add_course():
    data = request.json
    new_course = Course(name=data.get('name'))

    db.session.add(new_course)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Course added successfully'})

@routes.route('/delete-course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Course deleted successfully'})
    return jsonify({'error': 'Course not found'}), 404

# -------------------- SUBJECT FUNCTIONALITY -------------------- #

@routes.route('/subjects/<int:course_id>', methods=['GET'])
def get_subjects(course_id):
    subjects = Subject.query.filter_by(course_id=course_id).all()
    return jsonify([{'id': subject.id, 'name': subject.name} for subject in subjects])

@routes.route('/add-subject', methods=['POST'])
def add_subject():
    data = request.json
    new_subject = Subject(name=data.get('name'), course_id=data.get('course_id'))

    db.session.add(new_subject)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Subject added successfully'})

@routes.route('/delete-subject/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subject deleted successfully'})
    return jsonify({'error': 'Subject not found'}), 404

# -------------------- CHAPTER FUNCTIONALITY -------------------- #

@routes.route('/chapters/<int:subject_id>', methods=['GET'])
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([{'id': chapter.id, 'name': chapter.name} for chapter in chapters])

@routes.route('/add-chapter', methods=['POST'])
def add_chapter():
    data = request.json
    new_chapter = Chapter(name=data.get('name'), subject_id=data.get('subject_id'))

    db.session.add(new_chapter)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chapter added successfully'})

@routes.route('/delete-chapter/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Chapter deleted successfully'})
    return jsonify({'error': 'Chapter not found'}), 404

@routes.route('/change-password', methods=['POST'])
def change_password():
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({'error': 'Username and password are required.'})

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user:
            # Update password
            cursor.execute('UPDATE user SET password = ? WHERE username = ?', (new_password, username))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Password updated successfully.'})
        else:
            conn.close()
            return jsonify({'error': 'Username not found.'})

    except Exception as e:
        return jsonify({'error': str(e)})
    



@routes.route('/api/questions', methods=['POST'])
def add_question():
    data = request.json

    # Step 1: Add the Question
    new_question = Question(
        text=data.get('question'),
        chapter_id=data.get('chapter')
    )
    db.session.add(new_question)
    db.session.commit()

    # Step 2: Add Options
    options_data = data.get('options', [])
    correct_answer = data.get('correctAnswer')

    for option_text in options_data:
        is_correct = option_text == correct_answer
        new_option = Option(
            text=option_text,
            is_correct=is_correct,
            question_id=new_question.id  # Link options to the newly created question
        )
        db.session.add(new_option)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Question and options added successfully!',
        'question_id': new_question.id
    })

@routes.route('/get-questions', methods=['GET'])
@jwt_required()
def get_questions():
    
    quiz_name = request.args.get('quizName')
    duration = request.args.get('duration')
    questions_count = int(request.args.get('questions'))

    conn = get_db()
    questions = conn.execute('''
    SELECT q.id, q.text, o.id AS option_id, o.text AS option_text
FROM question q
JOIN option o ON q.id = o.question_id
WHERE q.id IN (
    SELECT id 
    FROM question 
    WHERE chapter_id = (
        SELECT id 
        FROM chapter 
        WHERE name = ?
    )
    LIMIT ?
)

''', (quiz_name, questions_count)).fetchall()

    conn.close()

    result = {}
    for row in questions:
        q_id = row['id']
        if q_id not in result:
            result[q_id] = {
                'id': q_id,
                'text': row['text'],
                'options': []
            }
        result[q_id]['options'].append({
            'id': row['option_id'],
            'text': row['option_text']
        })

    return jsonify(list(result.values()))

#----------------------------------Quiz submition---------------------------------
@routes.route('/submit-quiz', methods=['POST'])
@jwt_required()
def submit_quiz():
    identity = get_jwt_identity()  # Now in format "username:course"
    print("🔐 Protected Route - Token Data:", identity)

    try:
        username, course = identity.split(':')  # 🔥 Extract values from string
    except ValueError:
        return jsonify({"error": "Invalid token format"}), 400
    
    data = request.get_json()
    print("🔎 Received data:", data)
    
    # Data validation
    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400
    


    quiz_name = data.get('quizName')
    user_id = username
    user_answers = data.get('userAnswers', {})

    if not quiz_name or not user_id:
        return jsonify({"error": "quizName or userID missing"}), 400

    if not isinstance(user_answers, dict):
        return jsonify({"error": "Invalid data format for userAnswers"}), 400

    # Database connection
    try:
        conn = get_db()
    except Exception as e:
        return jsonify({"error": f"Database connection error: {str(e)}"}), 500

    # Fetch correct answers
    correct_answers = conn.execute('''
        SELECT q.id, o.text AS correct_answer
        FROM question q
        JOIN option o ON q.id = o.question_id
        WHERE o.is_correct = 1 AND q.chapter_id = (
            SELECT id FROM chapter WHERE name = ?
        )
    ''', (quiz_name,)).fetchall()

    if not correct_answers:
        return jsonify({"error": "No questions found for this quiz"}), 404

    correct_answer_dict = {str(row['id']): row['correct_answer'] for row in correct_answers}

    # Calculate score
    score = sum(1 for q_id, selected_option in user_answers.items()
                if correct_answer_dict.get(q_id) == selected_option)

    # Insert quiz result
    conn.execute('''
        INSERT INTO quiz_result (user_id, quiz_name, duration, questions_count, score, submission_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        quiz_name,
        data.get('duration', 0),
        len(correct_answers),
        score,
        datetime.now(timezone.utc)
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Quiz submitted successfully!", "score": score})

#---------------------------------------------------------------------------------------------------------
@routes.route('/attempted-quizzes', methods=['GET'])
@jwt_required()
def get_attempted_quizzes():
    try:
        identity = get_jwt_identity()  # Now in format "username:course"
        print("🔐 Protected Route - Token Data:", identity)

   
        username, course = identity.split(':')
        conn = get_db()
        quizzes = conn.execute('SELECT quiz_name FROM quiz_result where user_id=?',(username,)).fetchall()
        conn.close()

        quiz_list = [quiz['quiz_name'] for quiz in quizzes]
        return jsonify({'attempted_quizzes': quiz_list})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route 2: Fetch Quizzes for a Specific User (Card 2 - Dropdown)
@routes.route('/user-quizzes', methods=['GET'])
@jwt_required()
def get_user_quizzes():
    try:
        identity = get_jwt_identity()  # Now in format "username:course"
        print("🔐 Protected Route - Token Data:", identity)

   
        username, course = identity.split(':')  # 🔥 Extract values from string
    
        


        user_id = username
        conn = get_db()
        quizzes = conn.execute('SELECT id, quiz_name FROM quiz_result WHERE user_id = ?', (user_id,)).fetchall()
        conn.close()

        quiz_list = [{'id': quiz['id'], 'quiz_name': quiz['quiz_name']} for quiz in quizzes]  # ✅ Include ID
        return jsonify({'user_quizzes': quiz_list})   

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route 3: Fetch Quiz Details Based on Quiz ID (Card 2 - Details Display)
@routes.route('/quiz-details/<int:quiz_id>', methods=['GET'])
def get_quiz_details(quiz_id):
    try:
        conn = get_db()
        quiz_details = conn.execute(
            '''
            SELECT quiz_name, score, duration, questions_count
            FROM quiz_result
            WHERE id = ?
            ''',
            (quiz_id,)
        ).fetchone()

        conn.close()

        if quiz_details:
            return jsonify({
                'quiz_name': quiz_details['quiz_name'],
                'score': quiz_details['score'],
                'duration': quiz_details['duration'],
                'questions_attempted': quiz_details['questions_count']
            })
        else:
            return jsonify({'error': 'Quiz not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/download-report')
@jwt_required()
def download_report():

    identity = get_jwt_identity()  # Now in format "username:course"
    print("🔐 Protected Route - Token Data:", identity)

    try:
        username, course = identity.split(':')  # 🔥 Extract values from string
    except ValueError:
        return jsonify({"error": "Invalid token format"}), 400
    user_id = username # Fetch user ID from query parameter

    

    conn = get_db()
    cursor = conn.cursor()

    # Fetch user quiz data
    cursor.execute("""
        SELECT r.quiz_name, r.score, r.duration , r.submission_time
        FROM quiz_result r
        WHERE r.user_id = ?
    """, (user_id,))

    report_data = cursor.fetchall()
    conn.close()

    if not report_data:
        return jsonify({"error": "No data found for this user"}), 404

    # Create CSV data
    output = io.StringIO()
    csv_writer = csv.writer(output)

    # CSV Headers
    csv_writer.writerow(["Quiz Name", "Score", "Duration"])

    # CSV Data Rows
    for row in report_data:
        csv_writer.writerow([row["quiz_name"], row["score"], row["duration"],row["submission_time"]])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'report_{user_id}.csv'
    )
#---------------------------------------------------------------------------------------***

@routes.route('/quiz-summary', methods=['GET'])
def get_quiz_summary():
    try:
        # Establish connection
        conn = get_db()
        cursor = conn.cursor()

        # Raw SQL query to get distinct user attempts per quiz_name
        query = """
        SELECT quiz_name, COUNT(user_id) AS user_attempts
        FROM quiz_result
        GROUP BY quiz_name;
        """

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        quiz_data = cursor.fetchall()

        # Format the results into a dictionary
        quiz_summary = [{"quiz_name": quiz[0], "user_attempts": quiz[1]} for quiz in quiz_data]

        # Close the cursor and connection
        cursor.close()

        return jsonify(quiz_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/user-summary', methods=['GET'])
def get_user_summary():   # <-- Fixed function name
    try:
        # Establish connection
        conn = get_db()
        cursor = conn.cursor()

        # Corrected SQL query with appropriate aggregation
        query = """
        SELECT user_id, quiz_name, MAX(duration) AS duration,
               MAX(questions_count) AS questions_count,
               MAX(score) AS score
        FROM quiz_result
        GROUP BY user_id, quiz_name;
        """

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        quiz_data = cursor.fetchall()

        # Format the results into a dictionary
        user_summary = [
            {"user_id": quiz[0], "quiz_name": quiz[1], "duration": quiz[2],
             "questions_count": quiz[3], "score": quiz[4]}
            for quiz in quiz_data
        ]

        # Close the cursor and connection
        cursor.close()

        return jsonify(user_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#******************************************************************************************************
#******************************************************************************************************

@routes.route('/send-reminders', methods=['POST'])
def send_reminders():
    conn = get_db()
    cursor = conn.cursor()

    # Fetch all user emails from the user table
    cursor.execute("SELECT email FROM user")
    user_emails = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    # Send reminder emails to all fetched users
    for email in user_emails:
        send_email_reminder(email)

    return jsonify({"message": "Reminders sent successfully!"})

# Function to send reminder emails
def send_email_reminder(user_email):
    sender_email = "ujjawalrauniyar2004@gmail.com"  # Replace with your email
    sender_password = "cifylmcwkflrwwes"  # Replace with your email password (use an app password for Gmail)

    subject = "Daily Quiz Reminder"
    body = "Hello, don't forget to visit the platform to participate in quizzes and improve your knowledge!"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            print(f"Reminder sent to {user_email}")
    except Exception as e:
        print(f"Error sending email to {user_email}: {e}")




#*****************************************************************************
#******************************************************************************

@routes.route('/edit-course/<int:course_id>', methods=['PUT'])
def edit_course(course_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE course SET name = ? WHERE id = ?', (data.get('name'), course_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Course updated successfully'})

# Edit Subject Route
@routes.route('/edit-subject/<int:subject_id>', methods=['PUT'])
def edit_subject(subject_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE subject SET name = ? WHERE id = ?', (data.get('name'), subject_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Subject updated successfully'})

# Edit Chapter Route
@routes.route('/edit-chapter/<int:chapter_id>', methods=['PUT'])
def edit_chapter(chapter_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE chapter SET name = ? WHERE id = ?', (data.get('name'), chapter_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Chapter updated successfully'})



#************************************************************************************
@routes.route('/api/get_questions/<int:chapter_id>', methods=['GET'])
def get_questions_by_chapter(chapter_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    query = """
    SELECT 
        q.id, 
        q.text, 
        o.text AS option_text, 
        o.is_correct 
    FROM 
        question q 
    JOIN 
        option o ON q.id = o.question_id 
    WHERE 
        q.chapter_id = ?
    """

    cursor.execute(query, (chapter_id,))
    data = cursor.fetchall()

    questions = {}
    for row in data:
        question_id, question_text, option_text, is_correct = row
        if question_id not in questions:
            questions[question_id] = {
                'id': question_id,
                'text': question_text,
                'options': [],
                'correctAnswer': None  # Set to None initially
            }
        questions[question_id]['options'].append({'text': option_text})

        # Identify the correct answer
        if is_correct == 1:
            questions[question_id]['correctAnswer'] = option_text  

    connection.close()
    return jsonify(list(questions.values()))
def get_questions(chapter_id):
    try:
        questions = get_questions_by_chapter(chapter_id)
        return jsonify(questions)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch questions', 'details': str(e)}), 500

@routes.route('/api/edit_question/<int:question_id>', methods=['PUT'])
def edit_question(question_id):
    data = request.json

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    question.text = data['question']
    Option.query.filter_by(question_id=question.id).delete()  # Remove old options

    for option_text in data['options']:
        is_correct = (option_text == data['correctAnswer'])
        new_option = Option(text=option_text, is_correct=is_correct, question_id=question.id)
        db.session.add(new_option)

    db.session.commit()
    return jsonify({"message": "Question updated successfully!"})

# ----------------------- DELETE ROUTES -----------------------
@routes.route('/api/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    Option.query.filter_by(question_id=question.id).delete()
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully!"})

app.register_blueprint(routes)
if __name__ == '__main__':
    app.run(debug=True)