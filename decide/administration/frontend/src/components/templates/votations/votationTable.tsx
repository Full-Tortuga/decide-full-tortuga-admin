import React from "react";
import { GridColDef } from "@mui/x-data-grid";

import { votationType } from "types";
import { Table } from "components/02-molecules";

// todo: set correct columns

const columns: GridColDef[] = [
  {
    field: "name",
    headerName: "Name",
    width: 110,
  },
  {
    field: "description",
    headerName: "Description",
    width: 200,
  },
  {
    field: "question",
    headerName: "Question",
    width: 200,
  },
  {
    field: "census",
    headerName: "Census",
    width: 110,
  },
  {
    field: "auth",
    headerName: "Auth",
    width: 110,
  },
];

const Component = (props: { votations: votationType.Votation[]; setSelected: any }) => {
  return (
    <Table
      rows={props.votations}
      columns={columns}
      setSelected={props.setSelected}
    />
  );
};

export default Component;
