import { axios } from "api/config";


const baseApi = {
  //        KEYS OPERATIONS
  //Bulk operation
  getKeys: () => axios.get("/base/key"),
  deleteKeys: () => axios.delete(`/base/key/`),

  //Individual operations
  getKey: (id: string) => axios.get(`/base/key/${id}`),
  createKey: (key: any) => axios.post("/base/key/", key),
  updateKey: (key: any) => axios.put(`/base/key/${key.id}`, key),
  deleteKey: (id: string) => axios.delete(`/base/key/${id}`),  


  //        AUTH OPERATIONS
  //Bulk operation
  getAuths: () => axios.get("/base/auth"),
  createAuth: (auth: any) => axios.post("/base/auth/", auth),
  deleteAuths: () => axios.delete(`/base/auth`),

  //Individual operations
  getAuth: (id: string) => axios.get(`/base/auth/${id}`),
  updateAuth: (auth: any) => axios.put(`/base/auth/${auth.id}`, auth),
  deleteAuth: (id: string) => axios.delete(`/base/auth/${id}`)
};


export default baseApi;