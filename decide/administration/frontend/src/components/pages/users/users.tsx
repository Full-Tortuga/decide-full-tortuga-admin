import React from "react";
import { Delete } from "@mui/icons-material";

import { userApi } from "api";
import { userType } from "types";

import { ActionBar } from "components/03-organisms";
import { NewUserForm, UserTable } from "components/templates/users";

import Page from "../page";

// todo: fetch users from api and set rows to the response
const rows = [
  { id: 1, lastName: "Snow", firstName: "Jon", age: 35 },
  { id: 2, lastName: "Lannister", firstName: "Cersei", age: 42 },
  { id: 3, lastName: "Lannister", firstName: "Jaime", age: 45 },
  { id: 4, lastName: "Stark", firstName: "Arya", age: 16 },
  { id: 5, lastName: "Targaryen", firstName: "Daenerys", age: null },
  { id: 6, lastName: "Melisandre", firstName: null, age: 150 },
  { id: 7, lastName: "Clifford", firstName: "Ferrara", age: 44 },
  { id: 8, lastName: "Frances", firstName: "Rossini", age: 36 },
  { id: 9, lastName: "Roxie", firstName: "Harvey", age: 65 },
];

const UsersPage = () => {
  const [users, setUsers] = React.useState(rows);
  const [selected, setSelected] = React.useState([]);

  React.useEffect(() => {
    userApi.getUsers().then((response) => {
      console.log(response);
      setUsers(rows);
    });
  }, []);

  const idList = React.useMemo(
    () => selected.map((user: userType.User) => user.id),
    [selected]
  );

  const handleDelete = () => {
    console.log(idList);
  };

  return (
    <>
      <Page title="Users">
        <UserTable users={users || rows} setSelected={setSelected} />
      </Page>
      <ActionBar
        selection={selected}
        actions={[
          <NewUserForm
            initialUser={selected.length === 1 ? selected[0] : undefined}
          />,
        ]}
        bulkActions={[
          {
            icon: <Delete />,
            title: "Delete",
            onClick: () => {
              console.log("delete");
              handleDelete();
            },
          },
        ]}
      />
    </>
  );
};

export default UsersPage;
