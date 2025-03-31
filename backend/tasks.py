from celery import Celery
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def send_monthly_report():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch user details and quiz performance
    cursor.execute("""
        SELECT 
    user.email, 
    user.name, 
    COUNT(quiz_result.id) AS total_quizzes,
    SUM(quiz_result.score) AS total_score,
    AVG(quiz_result.score) AS avg_score
FROM 
    user
JOIN 
    quiz_result ON user.id = quiz_result.user_id
WHERE 
    datetime(quiz_result.submission_time) >= datetime('now', '-1 month')
GROUP BY 
    user.id;
    """)
    
    for email, name, total_quizzes, total_score, avg_score in cursor.fetchall():
        send_report_email(email, name, total_quizzes, total_score, avg_score)

    conn.close()

def send_report_email(email, name, total_quizzes, total_score, avg_score):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    # Email content in HTML
    body = f"""
    <html>
    <body>
        <h2>Hi {name},</h2>
        <p>Here’s your quiz performance for this month:</p>
        <ul>
            <li>Total Quizzes: <strong>{total_quizzes}</strong></li>
            <li>Total Score: <strong>{total_score}</strong></li>
            <li>Average Score: <strong>{round(avg_score, 2)}</strong></li>
        </ul>
        <p>Good luck for the next month! 😊</p>
    </body>
    </html>
    """

    # Email structure
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "📊 Monthly Quiz Activity Report"
    msg.attach(MIMEText(body, 'html'))

    # Email sending logic
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            print(f"✅ Report sent to {email}")
    except Exception as e:
        print(f"❌ Error sending report to {email}: {e}")
