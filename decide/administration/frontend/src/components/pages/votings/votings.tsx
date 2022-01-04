import React from "react";
import { Delete, Refresh, PlayArrow, Pause } from "@mui/icons-material";

import { votingType } from "types";
import { votingApi } from "api"

import { ActionBar } from "components/03-organisms";
import { VotingTable, VotingForm } from "components/templates";
import Page from "../page";
import { utils } from "utils";

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
  // const selectionState = React.useMemo(() => {
  //   const checkOptions = (active: number) => {
  //     if (active === selected.length && selected.length > 0) return "true";
  //     else if (active === 0) return "false";
  //     else return "mixed";
  //   };

  //   const activeNumber = selected.filter(
  //     (user: userType.User) => user.is_active
  //   ).length;
  //   const staffNumber = selected.filter(
  //     (user: userType.User) => user.is_staff
  //   ).length;
  //   const suNumber = selected.filter(
  //     (user: userType.User) => user.is_superuser
  //   ).length;

  //   return {
  //     active: getStatus(votings),
  //   };
  // }, [selected]);

  const handleDelete = () => {
    // todo: remove this 2 lines and uncomment the lines after
    console.log(idList);
    refetchVotings();
    // votingApi.deleteVotings(idList).then((response) => {
    //   console.log(response);
    //   refetchVotings();
    // });
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
          // {
          //   icon:
          //     selectionState.active === "true" ? (
          //       <Pause color="warning" />
          //     ) : (
          //       <PlayArrow />
          //     ),
          //   title:
          //     selectionState.active === "true"
          //       ? "Mark as Inactive"
          //       : "Mark as Active",
          //   disabled: selectionState.active === "mixed",
          //   onClick: () => {
          //     console.log("switch active");
          //     // selectionState.active === "true"
          //     //   ? handleChangeActive(false)
          //     //   : handleChangeActive(true);
          //   },
          // },
        ]}
      />
    </>
  );
};

export default VotingsPage;
