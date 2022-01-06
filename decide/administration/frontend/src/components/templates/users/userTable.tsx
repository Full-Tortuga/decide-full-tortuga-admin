import React from "react";
import { GridColDef } from "@mui/x-data-grid";

import { userType } from "types";
import { Table } from "components/02-molecules";

const columns: GridColDef[] = [
  {
    field: "username",
    headerName: "Username",
    minWidth: 140,
  },
  {
    field: "first_name",
    headerName: "First name",
    minWidth: 170,
  },
  {
    field: "last_name",
    headerName: "Last name",
    minWidth: 170,
  },
  {
    field: "email",
    headerName: "Email",
    minWidth: 230,
  },
  {
    field: "is_active",
    headerName: "Active",
    minWidth: 80,
    align: "center",
    valueFormatter: (params) => (params.value ? "✔" : "✘"),
  },
  {
    field: "is_staff",
    headerName: "Staff",
    minWidth: 80,
    align: "center",
    valueFormatter: (params) => (params.value ? "✔" : "✘"),
  },
  {
    field: "is_superuser",
    headerName: "Superuser",
    minWidth: 120,
    align: "center",
    valueFormatter: (params) => (params.value ? "✔" : "✘"),
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
