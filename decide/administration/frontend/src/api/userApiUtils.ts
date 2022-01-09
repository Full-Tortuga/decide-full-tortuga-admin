import { axios } from "api/axios";
import { userType } from "types";

const userApi = {
  // bulk simple operations
  getUsers: () => axios.get("/users"),
  deleteUsers: (idList: number[]) =>
    axios.delete("/users", {
      data: { idList },
    }),

  // bulk role/status operations
  updateUsersActive: (idList: number[], value: boolean) =>
    axios.post("/users/state", {
      idList,
      state: "Active",
      value: value ? "True" : "False",
    }),
  updateUsersRole: (
    idList: number[],
    value: boolean,
    role: "Staff" | "Superuser"
  ) =>
    axios.post("/users/state", {
      idList,
      state: role,
      value: value ? "True" : "False",
    }),

  // individual simple operations
  getUser: (id: number) => axios.get(`/users/${id}`),
  createUser: (user: userType.User) => axios.post("/users", user),
  updateUser: (id: number, user: userType.User) =>
    axios.put(`/users/${id}`, user),
  deleteUser: (id: number) => axios.delete(`/users/${id}`),
};

export default userApi;
