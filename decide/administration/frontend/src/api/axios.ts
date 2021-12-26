import Axios from "axios";

import { sessionUtils } from "utils";

const API_URL = "http://localhost:8000/administration/api";

export const axios = Axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Auth interceptor (logout)
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 403) {
      sessionUtils.removeToken();
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// Error handling interceptor
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // todo: handle errors
    const message = error.response?.data?.message || error.message;
    console.warn(message);
    return Promise.reject(error);
  }
);
