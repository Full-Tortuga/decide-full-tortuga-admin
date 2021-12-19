import { axios } from "api/axios";
import { userType } from "types";

const userApi = {
  // bulk simple operations
  getUsers: () => axios.get("/users"),
  deleteUsers: (idList: number[]) =>
    axios.delete("/users", { data: { idList: idList.join(",") } }),

  // bulk role/status operations
  updateUsersActive: (idList: number[], value: boolean) =>
    axios.post("/users/state", {
      idList: idList.join(","),
      state: "Active",
      value: value ? "True" : "False",
    }),
  updateUsersRole: (
    idList: number[],
    value: boolean,
    role: "Staff" | "Superuser"
  ) =>
    axios.post("/users/state", {
      idList: idList.join(","),
      state: role,
      value: value ? "True" : "False",
    }),

  // individual simple operations
  getUser: (id: string) => axios.get(`/users/${id}`),
  createUser: (user: userType.User) => axios.post("/users", user),
  updateUser: (user: userType.User) => axios.put(`/users/${user.id}`, user),
  deleteUser: (id: string) => axios.delete(`/users/${id}`),
};

export default userApi;
