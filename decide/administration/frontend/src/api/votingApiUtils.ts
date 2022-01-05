import { axios } from "api/axios";
import { Question, Voting } from "types/voting";


const votingApi = {

    //QUESTION API
    //Bulk Operations
    getQuestions: () => axios.get("/voting/question"),
    deleteQuestions: (idList: number[]) => axios.delete("/voting/questions", {
        data: { idList: idList },
    }),
    deleteAllQuestions: () => axios.delete(`/voting/question`), 
    
    //Individual Operations
    getQuestion: (questionId: number) => axios.get(`/voting/question/${questionId}/`),
    createQuestion: (question: Question) => axios.post("/voting/question/", question),
    updateQuestion: (question: Question, questionId: number) => axios.put(`/voting/question/${questionId}/`, question),
    deleteQuestion: (questionId: number) => axios.delete(`/voting/question/${questionId}/`),  

    //VOTING API
    //Bulk Operations   
    getVotings:() => axios.get(`/votings`),
    deleteVotings: (idList: number[]) => axios.delete("/votings",{
         data: { idList: idList },}
    ),
    deleteAllVotings: () => axios.delete(`/votings`), 
    
    startVotings:(
        idList:number[]       
    ) => 
    axios.put("/votings", {
        idList: idList,
        action: "start",        
    }),

    stopVotings:(
        idList:number[]       
    ) => 
    axios.put("/votings", {
        idList: idList,
        action: "stop",        
    }),

    tallyVotings:(
        idList:number[]       
    ) => 
    axios.put("/votings", {
        idList: idList,
        action: "tally",        
    }),
    
    //Individual Operations
    getVoting: (votingId: number) => axios.get(`/votings/${votingId}/`),
    createVoting: (voting: Voting) => axios.post("/votings", voting),
    updateVoting: (voting: Voting, votingId: number) => axios.put(`/votings/${votingId}/`, voting),
    deleteVoting: (votingId: number) => axios.delete(`/votings/${votingId}/`),  
};

export default votingApi;

