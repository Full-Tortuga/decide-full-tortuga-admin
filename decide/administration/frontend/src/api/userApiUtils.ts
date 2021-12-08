import { axios } from "api/config";

const userApi = {
  // bulk operations
  getUsers: () => axios.get("/users"),

  // individual operations
  getUser: (id: string) => axios.get(`/users/${id}`),
  createUser: (user: any) => axios.post("/users", user),
  updateUser: (user: any) => axios.put(`/users/${user.id}`, user),
  deleteUser: (id: string) => axios.delete(`/users/${id}`),
};

export default userApi;
