import * as React from "react";

import { DataGrid, GridColDef } from "@mui/x-data-grid";

const Component = (props: { rows: any[]; columns: GridColDef[] }) => {
  return (
    <div className="w-full">
      <DataGrid
        rows={props.rows}
        columns={props.columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        checkboxSelection
      />
    </div>
  );
};

export default Component;
