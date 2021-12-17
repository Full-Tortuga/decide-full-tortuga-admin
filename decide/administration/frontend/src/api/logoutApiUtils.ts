import { axios } from "api/config";

const userApi = {
  getUser: () => axios.get(`api/auth/logout`),
};


export default userApi;