import React from "react";
import { GridColDef } from "@mui/x-data-grid";

import { userType } from "types";
import { Table } from "components/02-molecules";

// todo: set correct columns

const columns: GridColDef[] = [
  { field: "id", headerName: "ID" },
  {
    field: "firstName",
    headerName: "First name",
    width: 200,
  },
  {
    field: "lastName",
    headerName: "Last name",
    width: 200,
  },
  {
    field: "age",
    headerName: "Age",
    type: "number",
    width: 110,
  },
];

const Component = (props: { users: userType.User[] }) => {
  return <Table rows={props.users} columns={columns} />;
};

export default Component;
