import Axios, { AxiosRequestConfig } from "axios";

import { sessionUtils } from "utils";

const API_URL = "http://localhost:8000/administration/api/";

export const axios = Axios.create({
  baseURL: API_URL,
});

// Headers interceptor
axios.interceptors.request.use((config: AxiosRequestConfig) => {
  if (config.headers) {
    // content-type
    config.headers.Accept = "application/json";
    config.headers.ContentType = "application/json";
    config.headers["Access-Control-Allow-Origin"] = "*";
  }

  return config;
});

// Auth interceptor (logout)
axios.interceptors.response.use(
  (response) => {
    return response.data;
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
    return response.data;
  },
  (error) => {
    // todo: handle errors
    const message = error.response?.data?.message || error.message;
    console.warn(message);
    return Promise.reject(error);
  }
);
