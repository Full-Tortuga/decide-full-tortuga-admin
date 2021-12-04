import Axios, { AxiosRequestConfig } from "axios";
import { localStore } from "store";

const API_URL = "http://localhost:8000/administration/api/";

export const axios = Axios.create({
  baseURL: API_URL,
});

// Headers interceptor
axios.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStore.getToken();
  if (config.headers) {
    // auth
    if (token) config.headers.token = `${token}`;
    // content-type
    config.headers.Accept = "application/json";
    config.headers.ContentType = "application/json";
  }

  return config;
});

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
