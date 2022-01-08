import React from "react";
import { HowToVote, Person, Refresh } from "@mui/icons-material";

import { dashboardApi } from "api";
import { userType } from "types";

import { IconButton, StatBox } from "components/01-atoms";
import { Severity } from "components/01-atoms/Notification";

import Page from "../page";

type DashboardData = {
  session: userType.User;
  users: {
    total: number;
    active: number;
    admins: number;
    employees: number;
  };
  votings: {
    notStarted: number;
    inProgress: number;
    finished: number;
  };
};

const HomePage = () => {
  const [data, setData] = React.useState<DashboardData>();

  const [refetch, setRefetch] = React.useState(false);

  const refetchData = () => setRefetch(!refetch);

  const [notifications, setNotifications] = React.useState<
    { type: Severity; message: string }[]
  >([]);

  const notify = (type: Severity, message: string) => {
    setNotifications((prev) => [...prev, { type, message }]);
  };

  React.useEffect(() => {
    dashboardApi
      .getData()
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => notify("error", "Stats not fetched: " + error.message));
  }, [refetch]);

  const totalVotings = React.useMemo(
    () =>
      data?.votings
        ? Object.values(data.votings).reduce((acc, v) => acc + v, 0)
        : 0,
    [data]
  );

  return (
    <Page title="Home" notifications={notifications}>
      <div className="grid grid-cols-3 gap-7">
        <StatBox
          title="Active users"
          active={data?.users.active || 0}
          total={data?.users.total || 0}
          icon={<Person />}
          color="success"
        />
        <StatBox
          title="Employees"
          active={data?.users.employees || 0}
          total={data?.users.total || 0}
          icon={<Person />}
          color="primary"
        />
        <StatBox
          title="Admins"
          active={data?.users.admins || 0}
          total={data?.users.total || 0}
          icon={<Person />}
          color="primary"
        />
        <StatBox
          title="Votings not started"
          active={data?.votings.notStarted || 0}
          total={totalVotings}
          icon={<HowToVote />}
          color="primary"
        />
        <StatBox
          title="Votings in progress"
          active={data?.votings.inProgress || 0}
          total={totalVotings}
          icon={<HowToVote />}
          color="warning"
        />
        <StatBox
          title="Votings finished"
          active={data?.votings.finished || 0}
          total={totalVotings}
          icon={<HowToVote />}
          color="success"
        />
      </div>
      <IconButton icon={<Refresh />} title="Refetch" onClick={refetchData} />
    </Page>
  );
};

export default HomePage;
