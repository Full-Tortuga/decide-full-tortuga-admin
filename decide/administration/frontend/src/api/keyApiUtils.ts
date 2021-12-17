import { axios } from "api/config";


const keysApi = {
  //Bulk operation
  getKeys: () => axios.get("api/base/key"),
  deleteKeys: () => axios.delete(`api/base/key/`),

  //Individual operations
  getKey: (id: string) => axios.get(`api/base/key/${id}`),
  createKey: (key: any) => axios.post("api/base/key/", key),
  updateKey: (key: any) => axios.put(`api/base/key/${key.id}`, key),
  deleteKey: (id: string) => axios.delete(`api/base/key/${id}`),  
};


export default keysApi;