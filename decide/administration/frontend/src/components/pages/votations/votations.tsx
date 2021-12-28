import React from "react";
import {
  AdminPanelSettings,
  Delete,
  Pause,
  PlayArrow,
  Verified,
} from "@mui/icons-material";

import { votationType } from "types";

import { ActionBar } from "components/03-organisms";
import { NewVotationForm, VotationTable } from "components/templates/votations";

import Page from "../page";

const rows = [
  { id: 1, name: "Votacion 1", description: "Jon", question: "Pregunta 1", census: "Censo 1", auth: "Auth 1"},
  { id: 2, name: "Votacion 2", description: "Cersei", question: "Pregunta 2", census: "Censo 2", auth: "Auth 2"},
  { id: 3, name: "Votacion 3", description: "Jaime", question: "Pregunta 3", census: "Censo 3", auth: "Auth 3"},
  { id: 4, name: "Votacion 4", description: "Arya", question: "Pregunta 4", census: "Censo 4", auth: "Auth 4"},
  { id: 5, name: "Votacion 5", description: "Daenerys", question: "Pregunta 5", census: "Censo 5", auth: "Auth 5"},
  { id: 6, name: "Votacion 6", description: "Saliba", question: "Pregunta 6", census: "Censo 6", auth: "Auth 6"},
  { id: 7, name: "Votacion 7", description: "Ferrara", question: "Pregunta 7", census: "Censo 7", auth: "Auth 7"},
  { id: 8, name: "Votacion 8", description: "Rossini", question: "Pregunta 8", census: "Censo 8", auth: "Auth 8"},
  { id: 9, name: "Votacion 9", description: "Harvey", question: "Pregunta 9", census: "Censo 9", auth: "Auth 9"},
];

const VotationsPage = () => {
  //const [users, setVotations] = React.useState<votationType.Votation[]>([]);
  const [votations, setVotations] = React.useState(rows);

  const [selected, setSelected] = React.useState([]);
  const [refetch, setRefetch] = React.useState(false);

  const refetchVotations = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    //votationApi
      //.getVotations()
      //.then((response) => {
       // console.log(response);
      //  setVotations(response.data);
    //  })
    //.catch((error) => {
     //   console.log(error);
     // });
     setVotations(rows);
  }, [refetch]);

  const idList = React.useMemo(
    () => selected.map((votation: votationType.Votation) => votation.id),
    [selected]
  );

  const handleDelete = () => {
   // votationApi.deleteVotations(idList).then((response) => {
   //   console.log(response);
   //   refetchVotations();
   // });
  };

  return (
    <>
      <Page title="Votations">
        <VotationTable votations={votations || rows} setSelected={setSelected} />
      </Page>
      <ActionBar
        selection={selected}
        actions={[
          <NewVotationForm
            initialVotation={selected.length === 1 ? selected[0] : undefined}
          />,
        ]}
        bulkActions={[
          {
            icon: <Delete />,
            title: "Delete",
            onClick: () => {
              console.log("delete");
              handleDelete();
            },
          },
        ]}
      />
    </>
  );
};

export default VotationsPage;
