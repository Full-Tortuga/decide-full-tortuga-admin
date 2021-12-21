import * as React from "react";

import { DataGrid, GridColDef, GridSelectionModel } from "@mui/x-data-grid";

const Component = (props: {
  rows: any[];
  columns: GridColDef[];
  setSelected: any;
}) => {
  const filterRows = React.useCallback(
    (ids: any[]) => {
      console.log(ids);
      return props.rows.filter((row: any) => ids.includes(row.id));
    },
    [props.rows]
  );

  const [selectionModel, setSelectionModel] =
    React.useState<GridSelectionModel>([]);

  React.useEffect(() => {
    props.setSelected(filterRows(selectionModel));
  }, [selectionModel, filterRows]);

  return (
    <div className="w-full">
      <DataGrid
        autoHeight
        rows={props.rows}
        columns={props.columns}
        checkboxSelection
        selectionModel={selectionModel}
        onSelectionModelChange={(e) => setSelectionModel(e)}
      />
    </div>
  );
};

export default Component;
