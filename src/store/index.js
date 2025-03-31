import { createStore } from 'vuex';

export default createStore({
  state: {
    selectedAnswers: {}
  },
  mutations: {
    setSelectedAnswer(state, { questionId, optionId }) {
      state.selectedAnswers[questionId] = optionId;
    }
  },
  actions: {},
  modules: {}
});
