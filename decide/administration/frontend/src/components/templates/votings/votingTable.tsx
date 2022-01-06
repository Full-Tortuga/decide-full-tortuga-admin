import React from "react";
import { GridColDef } from "@mui/x-data-grid";
import { Chip, Tooltip } from "@mui/material";

import { votingType } from "types";
import { utils } from "utils";

import { Table } from "components/02-molecules";
import { IconButton } from "components/01-atoms";
import { HowToVoteOutlined, Visibility } from "@mui/icons-material";

const columns: GridColDef[] = [
  {
    field: "status",
    headerName: "Status",
    minWidth: 140,
    renderCell: (params) => {
      const status = utils.getStatus(params.row);
      const color = utils.getStatusColor(status || "");
      return <Chip label={status} color={color} />;
    },
  },
  {
    field: "name",
    headerName: "Name",
    minWidth: 140,
  },
  {
    field: "question",
    headerName: "Question",
    minWidth: 250,
    renderCell: (params) => {
      return (
        <Tooltip
          title={params.row.question.options
            .map(
              (o: { number: number; option: string }) =>
                `${o.number}: ${o.option}`
            )
            .join("; ")}
          arrow
        >
          <span>{params.row.question.desc}</span>
        </Tooltip>
      );
    },
  },
  {
    field: "start_date",
    headerName: "Start",
    minWidth: 140,
    valueFormatter: (params) =>
      params.value?.toLocaleString()?.split("T")[0] || "",
  },
  {
    field: "end_date",
    headerName: "End",
    minWidth: 140,
    valueFormatter: (params) =>
      params.value?.toLocaleString()?.split("T")[0] || "",
  },
  {
    field: "census",
    headerName: "Census",
    minWidth: 100,
    align: "center",
    valueFormatter: (params) => (params.value as number[])?.length,
  },
  {
    field: "tally",
    headerName: "Votes",
    minWidth: 100,
    align: "center",
    valueFormatter: (params) =>
      params.value === "[]"
        ? "0"
        : (params.value as string).replace("[", "").replace("]", ""),
  },
  {
    field: "link",
    headerName: "Links",
    align: "center",
    renderCell: (params) => {
      const status = utils.getStatus(params.row);
      return (
        <>
          {status === "In progress" && (
            <IconButton
              title={"Vote!"}
              icon={<HowToVoteOutlined />}
              onClick={() =>
                window.open(
                  "http://" +
                    window.location.hostname +
                    (window.location.port ? ":" + window.location.port : "") +
                    "/booth/" +
                    params.row.id
                )
              }
            />
          )}
          {status === "Finished" && (
            <IconButton
              title={"Results"}
              icon={<Visibility />}
              onClick={() =>
                window.open(
                  "http://" +
                    window.location.hostname +
                    (window.location.port ? ":" + window.location.port : "") +
                    "/visualizer/" +
                    params.row.id
                )
              }
            />
          )}
        </>
      );
    },
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
