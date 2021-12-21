import React from "react";
import { GridColDef } from "@mui/x-data-grid";

import { userType } from "types";
import { Table } from "components/02-molecules";

const columns: GridColDef[] = [
  {
    field: "username",
    headerName: "Username",
    width: 110,
  },
  {
    field: "first_name",
    headerName: "First name",
    width: 200,
  },
  {
    field: "last_name",
    headerName: "Last name",
    width: 200,
  },
  {
    field: "email",
    headerName: "Email",
    width: 110,
  },
  {
    field: "is_active",
    headerName: "Active",
    width: 110,
  },
  {
    field: "is_staff",
    headerName: "Staff",
    width: 110,
  },
  {
    field: "is_superuser",
    headerName: "Superuser",
    width: 110,
  },
];

const Component = (props: { users: userType.User[]; setSelected: any }) => {
  return (
    <Table
      rows={props.users}
      columns={columns}
      setSelected={props.setSelected}
    />
  );
};

export default Component;
