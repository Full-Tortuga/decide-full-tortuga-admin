import { useEffect, useState } from "react";
import Api from "../services/backend";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const Votes = () => {
  const [time, setTime] = useState(Date.now());
  const [state, setState] = useState({
    data: null,
  });

  useEffect(() => {
    const interval = setInterval(() => setTime(Date.now()), 1000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    Api.get_votes().then((res) => setState({ data: res }));
  }, [time]);

  return (
    <div>
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
          filterPlaceholder="Votación"
          field="name"
          header="Votación"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Pregunta"
          field="question.desc"
          header="Pregunta"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Descripción"
          field="desc"
          header="Descripción"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Fecha Inicio"
          field="start_date"
          header="Fecha Inicio"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Fecha Final"
          field="end_date"
          header="Fecha Final"
        ></Column>
        <Column
          sortable
          filter
          filterPlaceholder="Resultado"
          field="tally"
          header="Resultado de la Votación"
        ></Column>
      </DataTable>
    </div>
  );
};

export default Votes;
