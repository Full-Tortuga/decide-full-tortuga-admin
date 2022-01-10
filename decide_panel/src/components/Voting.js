import { useEffect, useState } from "react";
import Api from "../services/backend";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { ProgressBar } from "primereact/progressbar";

const Voting = () => {
  const [time, setTime] = useState(Date.now());
  const [errorConection, setErrorConection] = useState(null);
  const [state, setState] = useState({
    data: null,
  });

  function deleteErrorMessage() {
    setErrorConection(null);
  }

  useEffect(() => {
    const interval = setInterval(() => setTime(Date.now()), 1000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    deleteErrorMessage();
    Api.get_census(0)
      .then((res) => setState({ data: res }))
      .catch((error) => {
        setErrorConection(
          <div className="alert alert-dark">
            <strong>Error de conexión</strong>
            <ProgressBar
              mode="indeterminate"
              style={{ height: "6px" }}
            ></ProgressBar>
          </div>
        );
      });
  }, [time]);

  return (
    <div>
      {errorConection}
      <DataTable
        className="p-datatable-sm"
        paginator
        rows={5}
        value={state.data}
        header="Votaciones"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        rowsPerPageOptions={[5, 10, 25, 50]}
      >
        <Column
          sortable
          filter
          filterPlaceholder="Id del votante"
          field="id"
          header="Id del votante"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Nombre de usuario"
          field="username"
          header="Nombre de usuario"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Nombre"
          field="first_name"
          header="Nombre"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Apellidos"
          field="last_name"
          header="Apellidos"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Email"
          field="email"
          header="Email"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Género"
          field="gender"
          header="Género"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Región"
          field="region"
          header="Región"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Id de la votación"
          field="voting_id"
          header="Id de la votación"
        ></Column>
      </DataTable>
    </div>
  );
};

export default Voting;
