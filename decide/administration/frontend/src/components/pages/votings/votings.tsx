import React from "react";
import {
  Delete,
  Refresh,
  PlayArrow,
  Stop,
  HowToVoteOutlined,
  Cancel,
} from "@mui/icons-material";

import { votingType } from "types";
import { votingApi } from "api";
import { utils } from "utils";

import { Severity } from "components/01-atoms/Notification";
import { ActionBar } from "components/03-organisms";
import { VotingTable, VotingForm } from "components/templates";
import Page from "../page";

const VotingsPage = () => {
  const [votings, setVotings] = React.useState<votingType.Voting[]>([]);
  const [selected, setSelected] = React.useState([]);
  const [refetch, setRefetch] = React.useState(false);

  const [notifications, setNotifications] = React.useState<
    { type: Severity; message: string }[]
  >([]);

  const notify = (type: Severity, message: string) => {
    setNotifications((prev) => [...prev, { type, message }]);
  };

  const refetchVotings = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    votingApi
      .getVotings()
      .then((response) => {
        setVotings(response.data);
      })
      .catch((error) =>
        notify("error", "Votings not fetched: " + error.message)
      );
  }, [refetch]);

  const idList = React.useMemo(
    () => selected.map((voting: votingType.Voting) => voting.id || -1),
    [selected]
  );

  //See if votings have the same status
  const selectionState = React.useMemo(() => {
    const getSelectionStatus = (
      newNumber: number,
      inProgressNumber: number,
      finishedNumber: number
    ) => {
      if (newNumber === selected.length && selected.length > 0) return "new";
      else if (inProgressNumber === selected.length && selected.length > 0)
        return "in_progress";
      else if (finishedNumber === selected.length && selected.length > 0)
        return "finished";
      else return "mixed";
    };

    const newNumber = selected.filter(
      (voting: votingType.Voting) => utils.getStatus(voting) === "New"
    ).length;

    const inPogressNumber = selected.filter(
      (voting: votingType.Voting) => utils.getStatus(voting) === "In progress"
    ).length;

    const finishedNumber = selected.filter(
      (voting: votingType.Voting) => utils.getStatus(voting) === "Finished"
    ).length;

    return {
      status: getSelectionStatus(newNumber, inPogressNumber, finishedNumber),
    };
  }, [selected]);

  const handleDelete = () => {
    votingApi.deleteVotings(idList).then((response) => {
      console.log(response);
      refetchVotings();
    });
  };

  const handleChangeStatus = (status: string) => {
    if (status === "new")
      votingApi
        .startVotings(idList)
        .then((response) => {
          refetchVotings();
          notify("success", "Voting/s started");
        })
        .catch((error) =>
          notify("error", "Voting/s not started: " + error.message)
        );
    if (status === "in_progress")
      votingApi
        .stopVotings(idList)
        .then((response) => {
          refetchVotings();
          notify("success", "Voting/s stopped");
        })
        .catch((error) =>
          notify("error", "Voting/s not stopped: " + error.message)
        );
    if (status === "finished")
      votingApi
        .tallyVotings(idList)
        .then((response) => {
          refetchVotings();
          notify("success", "Voting/s tallied");
        })
        .catch((error) =>
          notify("error", "Voting/s not tallied: " + error.message)
        );
  };

  return (
    <>
      <Page title="Votings" notifications={notifications}>
        <VotingTable votings={votings} setSelected={setSelected} />
      </Page>
      <ActionBar
        selection={selected}
        actions={[
          <VotingForm
            initialVoting={selected.length === 1 ? selected[0] : undefined}
            refetch={refetchVotings}
            notify={notify}
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
              handleDelete();
            },
          },
          {
            icon:
              selectionState.status === "new" ? (
                <PlayArrow />
              ) : selectionState.status === "in_progress" ? (
                <Stop />
              ) : selectionState.status === "finished" ? (
                <HowToVoteOutlined />
              ) : (
                <Cancel />
              ),
            title:
              selectionState.status === "new"
                ? "Start"
                : selectionState.status === "in_progress"
                ? "Stop"
                : selectionState.status === "finished"
                ? "Tally"
                : "Cancel",
            disabled: selectionState.status === "mixed",
            onClick: () => {
              handleChangeStatus(selectionState.status);
            },
          },
        ]}
      />
    </>
  );
};

export default VotingsPage;
