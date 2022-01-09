import * as React from "react";

import { DataGrid, GridColDef, GridSelectionModel } from "@mui/x-data-grid";

const Component = (props: {
  rows: any[];
  columns: GridColDef[];
  setSelected: any;
  initialSelection?: number[];
}) => {
  const filterRows = React.useCallback(
    (ids: any[]) => {
      return props.rows.filter((row: any) => ids.includes(row.id));
    },
    [props.rows]
  );

  const [selectionModel, setSelectionModel] =
    React.useState<GridSelectionModel>(props.initialSelection || []);

  const updateSelectionModel = React.useCallback(
    (newSelection: GridSelectionModel) => {
      setSelectionModel(newSelection);
      props.setSelected(filterRows(newSelection));
    },
    [props, filterRows]
  );

  React.useEffect(() => {
    updateSelectionModel(selectionModel);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.rows]);

  return (
    <div className="w-full">
      <DataGrid
        autoHeight
        rows={props.rows}
        columns={props.columns}
        pageSize={10}
        checkboxSelection
        selectionModel={props.initialSelection || selectionModel}
        onSelectionModelChange={(e) => updateSelectionModel(e)}
      />
    </div>
  );
};

export default Component;
