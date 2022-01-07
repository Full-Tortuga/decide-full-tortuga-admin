import React from "react";
import { GridColDef } from "@mui/x-data-grid";

import { userType } from "types";
import { Table } from "components/02-molecules";
import { Chip } from "@mui/material";

const columns: GridColDef[] = [
  {
    field: "is_active",
    headerName: "Status",
    minWidth: 120,
    renderCell: (params) => {
      return (
        <Chip
          label={params.value ? "active" : "not-active"}
          color={params.value ? "success" : "warning"}
        />
      );
    },
  },
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
    field: "is_staff",
    headerName: "Staff",
    minWidth: 80,
    align: "center",
    renderCell: (params) => {
      return params.value && <Chip label="✔" color="primary" />;
    },
  },
  {
    field: "is_superuser",
    headerName: "Superuser",
    minWidth: 120,
    align: "center",
    renderCell: (params) => {
      return params.value && <Chip label="⛨" color="primary" />;
    },
  },
];

const Component = (props: {
  users: userType.User[];
  setSelected: any;
  initialSelection?: number[];
}) => {
  return (
    <Table
      rows={props.users}
      columns={columns}
      setSelected={props.setSelected}
      initialSelection={props.initialSelection}
    />
  );
};

export default Component;
