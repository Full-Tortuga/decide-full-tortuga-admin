import { axios } from "api/config";

const authApi = {
  login: (username: string, password: string) => {
    return axios.post("/auth/login", {
      username,
      password,
    });
  },
};

export default authApi;
