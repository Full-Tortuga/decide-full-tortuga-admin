import { axios } from "api/axios";
import { votingType } from "types";

const votingApi = {
  //QUESTION API
  //Bulk Operations
  getQuestions: () => axios.get("/voting/question"),
  deleteQuestions: (idList: number[]) =>
    axios.delete("/voting/questions", {
      data: { idList },
    }),
  deleteAllQuestions: () => axios.delete(`/voting/question`),

  //Individual Operations
  getQuestion: (questionId: number) =>
    axios.get(`/voting/question/${questionId}`),
  createQuestion: (question: votingType.Question) =>
    axios.post("/voting/question/", question),
  updateQuestion: (question: votingType.Question, questionId: number) =>
    axios.put(`/voting/question/${questionId}`, question),
  deleteQuestion: (questionId: number) =>
    axios.delete(`/voting/question/${questionId}`),

  //VOTING API
  //Bulk Operations
  getVotings: () => axios.get(`/votings`),
  deleteVotings: (idList: number[]) =>
    axios.delete("/votings", {
      data: { idList },
    }),
  deleteAllVotings: () => axios.delete(`/votings`),

  startVotings: (idList: number[]) =>
    axios.put("/votings", {
      idList,
      action: "start",
    }),

  stopVotings: (idList: number[]) =>
    axios.put("/votings", {
      idList,
      action: "stop",
    }),

  tallyVotings: (idList: number[]) =>
    axios.put("/votings", {
      idList,
      action: "tally",
    }),

  //Individual Operations
  getVoting: (votingId: number) => axios.get(`/votings/${votingId}`),
  createVoting: (voting: votingType.VotingFormFields) =>
    axios.post("/votings", voting),
  updateVoting: (voting: votingType.VotingFormFields, votingId: number) =>
    axios.put(`/votings/${votingId}`, voting),
  deleteVoting: (votingId: number) => axios.delete(`/votings/${votingId}`),
};

export default votingApi;
