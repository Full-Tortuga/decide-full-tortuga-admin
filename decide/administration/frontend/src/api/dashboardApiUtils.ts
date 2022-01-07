import { axios } from "api/axios";

const dashboardApi = {
  getData: () => {
    return axios.get("/dashboard");
  },
};

export default dashboardApi;
