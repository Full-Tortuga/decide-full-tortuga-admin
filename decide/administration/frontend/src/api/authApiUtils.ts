import { axios } from "api/axios";

const authApi = {
  login: (username: string, password: string) => {
    return axios.post("/auth/login", {
      username,
      password,
    });
  },
  logout: () => {
    return axios.post("/auth/logout");
  },
};

export default authApi;
