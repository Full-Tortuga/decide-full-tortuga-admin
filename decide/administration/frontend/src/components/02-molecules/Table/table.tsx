import * as React from "react";

import { DataGrid, GridColDef } from "@mui/x-data-grid";

const Component = (props: {
  rows: any[];
  columns: GridColDef[];
  setSelected: any;
}) => {
  const filterRows = (ids: any[]) => {
    return props.rows.filter((row: any) => ids.includes(row.id));
  };

  return (
    <div className="w-full">
      <DataGrid
        autoHeight
        rows={props.rows}
        columns={props.columns}
        checkboxSelection
        onSelectionModelChange={(e) => props.setSelected(filterRows(e))}
      />
    </div>
  );
};

export default Component;
