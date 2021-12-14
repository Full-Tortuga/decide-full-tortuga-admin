import { axios } from "api/config";

const userApi = {
  // bulk operations
  getUsers: () => axios.get("api/users"),
  //createUsers: (user: any) => axios.post("/users/", user),
  deleteUsers: () => axios.delete("api/users"),

  // individual operations
  getUser: (id: string) => axios.get(`api/users/${id}`),
  createUser: (user: any) => axios.post("api/users", user),
  updateUser: (user: any) => axios.put(`api/users/${user.id}`, user),
  deleteUser: (id: string) => axios.delete(`api/users/${id}`),
};


export default userApi;
