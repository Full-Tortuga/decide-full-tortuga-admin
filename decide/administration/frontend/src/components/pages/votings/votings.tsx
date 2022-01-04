import React from "react";
import { Delete, Refresh, PlayArrow, Pause, Stop} from "@mui/icons-material";

import { votingType } from "types";
import { votingApi } from "api"

import { ActionBar } from "components/03-organisms";
import { VotingTable, VotingForm } from "components/templates";
import Page from "../page";

const VotingsPage = () => {
  const [votings, setVotings] = React.useState<votingType.Voting[]>([]);
  const [selected, setSelected] = React.useState([]);
  const [refetch, setRefetch] = React.useState(false);

  const refetchVotings = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    votingApi
    .getVotings()
    .then((response) => {
     console.log(response);
     //response.data.setAttribute("status", utils.getStatus(response.data));
      setVotings(response.data);
      })
    .catch((error) => {
       console.log(error);
     });
  }, [refetch]);

  const idList = React.useMemo(
    () => selected.map((voting: votingType.Voting) => voting.id),
    [selected]
  );

  //See if votings have the same status
  const selectionState = React.useMemo(() => {
    const checkOptions = (start_date: number, end_date: number) => {
      if (start_date === 0 && end_date === 0) return "New";
      else if (start_date > 0 && end_date === 0) return "In progress";
      else if (start_date > 0 && end_date > 0) return "Finished";
    };

    const checkDisabled = ()=> {
      if (checkOptions.length === 0 && selected.length > 0) return "true";
      else if (checkOptions.length === 0) return "false";
      else return "mixed";
    };
    let start_date=0;
    if(selected.filter((voting: votingType.Voting) => voting.start_date
    )!==null){
      start_date = selected.filter(
        (voting: votingType.Voting) => voting.start_date
      ).length;
    }
        
    let end_date=0;
    if(selected.filter((voting: votingType.Voting) => voting.end_date
    )!==null){
      end_date = selected.filter(
        (voting: votingType.Voting) => voting.end_date
      ).length;
    }
    return {
      status: checkOptions(start_date,end_date),
      option: checkDisabled()
    };
  }, [selected]);

  

  const handleDelete = () => {
    console.log(idList);
    refetchVotings();
     votingApi.deleteVotings(idList).then((response) => {
       console.log(response);
       refetchVotings();
     });
  };

  const handleChangeActive = (status: string) => {
    console.log(idList);
    if(status === "New"){
      votingApi.startVotings(idList).then((response) => {
        console.log(response);
        refetchVotings();
      });
    }else if (status === "In progress"){
      votingApi.stopVotings(idList).then((response) => {
        console.log(response);
        refetchVotings();
      });
    }else{
      votingApi.tallyVotings(idList).then((response) => {
        console.log(response);
        refetchVotings();
      });
    }

  };

  return (
    <>
      <Page title="Votings">
        <VotingTable votings={votings} setSelected={setSelected} />
      </Page>
      <ActionBar
        selection={selected}
        actions={[
          <VotingForm
            initialVoting={selected.length === 1 ? selected[0] : undefined}
            refetch={refetchVotings}
          />,
        ]}
        individualActions={[
          {
            icon: <Refresh />,
            title: "Refresh",
            onClick: () => refetchVotings(),
          },
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
          {
            icon:
              selectionState.status === "New" ? (
                <PlayArrow />

              ) : (selectionState.status === "In progress" ) ? (
                <Pause color="warning" />

              ) :(
                <Stop />
              ),
            title:
              selectionState.status === "New"
                ? "Start voting"
                : (selectionState.status === "In progress") 
                ? ("Stop voting") : (
                  "Tally voting"
                ),
            disabled: selectionState.option === "mixed",
            onClick: () => {
              console.log("switch active");
              selectionState.status === "New"
                ? handleChangeActive("New") : (selectionState.status === "In progress") 
                ? (handleChangeActive("In progress")) 
                : handleChangeActive("Finished");
            },
          },
        
        ]}
      />
    </>
  );
};

export default VotingsPage;
