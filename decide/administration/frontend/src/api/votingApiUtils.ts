import { axios } from "api/axios";
import { Question, Voting } from "types/voting";


const votingApi = {

    //QUESTION API
    //Bulk Operations
    getQuestions: () => axios.get("/voting/question"),
    deleteQuestions: (idList: any) => axios.delete("/voting/questions", idList),
    deleteAllQuestions: () => axios.delete(`/voting/question`), 
    
    //Individual Operations
    getQuestion: (question_id: number) => axios.get(`/voting/question/${question_id}`),
    createQuestion: (question: Question) => axios.post("/voting/question/", question),
    updateQuestion: (question: Question, question_id: number) => axios.put(`/voting/question/${question_id}`, question),
    deleteQuestion: (question_id: number) => axios.delete(`/voting/question/${question_id}`),  


    //VOTING API
    //Bulk Operations   
    getVotings:() => axios.get(`/votings`),
    deleteVotings: (idList: any) => axios.delete("/votings", idList),
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
    getVoting: (voting_id: number) => axios.get(`/votings/${voting_id}`),
    createVoting: (voting: Voting) => axios.post("/votings", voting),
    deleteVoting: (voting_id: number) => axios.delete(`/votings/${voting_id}`),  
};

export default votingApi;

