import React from "react";
import { GridColDef } from "@mui/x-data-grid";
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';

import { votingType } from "types";
import { utils } from "utils";

import { Table } from "components/02-molecules";

const columns: GridColDef[] = [
  {
    field: "status",
    headerName: "Status",
    minWidth: 140,
    renderCell: (params) => {
      console.log(params.row)
      return utils.getStatus(params.row)
    }
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
    field: "question",
    headerName: "Question",
    minWidth: 250,
    renderCell: (params) => {
      return (
        <Tooltip title={params.row['question']['desc']} arrow>
        <Button>{params.row['question']['desc']}</Button>
        </Tooltip>
      );
    }
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
    valueFormatter: (params) => (params.value === "[]" ? "✘" : params.value),

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
