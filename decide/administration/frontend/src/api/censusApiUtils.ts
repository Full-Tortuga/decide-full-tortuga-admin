import { axios } from "api/axios";
import { Census } from "types/census";


const censusApi = {
  //Bulk operation
  getCensuss: () => axios.get("/census"),
  deleteCensuss: () => axios.delete(`/census`), 
  

  //Individual operations
  getCensus: (id: string) => axios.get(`/census/${id}`),
  createCensus: (census: Census) => axios.post("/census/", census),
  updateCensus: (census: Census) => axios.put(`/census/${census.id}`, census),
  deleteCensus: (id: string) => axios.delete(`/census/${id}`),  
  };


export default censusApi;