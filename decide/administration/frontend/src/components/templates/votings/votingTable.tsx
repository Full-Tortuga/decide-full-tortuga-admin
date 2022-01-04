import React from "react";
import { GridColDef } from "@mui/x-data-grid";

import { votingType } from "types";

import { Table } from "components/02-molecules";

const columns: GridColDef[] = [
  {
    field: "status",
    headerName: "Status",
    minWidth: 140,
    valueFormatter: (params) => (params.value)
  },
  {
    field: "name",
    headerName: "Name",
    minWidth: 140,
  },
  {
    field: "desc",
    headerName: "Description",
    minWidth: 250,
  },
  {
    //TODO GET QUESTION DESCRIPTION AND OPTIONS
    field: "question.desc",
    headerName: "Question",
    minWidth: 250,
  },
  {
    field: "start_date",
    headerName: "Start",
    minWidth: 140,
  },
  {
    field: "end_date",
    headerName: "End",
    minWidth: 140,
  },
  {
    field: "tally",
    headerName: "Tally",
    minWidth: 100,
    align: "center",
  },
];

const Component = (props: {
  votings: votingType.Voting[];
  setSelected: any;
}) => {
  return (
    <Table
      rows={props.votings}
      columns={columns}
      setSelected={props.setSelected}
    />
  );
};

export default Component;
