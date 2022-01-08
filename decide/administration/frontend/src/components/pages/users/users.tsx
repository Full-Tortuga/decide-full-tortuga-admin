import React from "react";
import {
  AdminPanelSettings,
  Delete,
  Pause,
  PlayArrow,
  Refresh,
  Verified,
} from "@mui/icons-material";

import { userApi } from "api";
import { userType } from "types";

import { Severity } from "components/01-atoms/Notification";
import { ActionBar } from "components/03-organisms";
import { UserForm, UserTable } from "components/templates";

import Page from "../page";

const UsersPage = () => {
  const [users, setUsers] = React.useState<userType.User[]>([]);
  const [selected, setSelected] = React.useState([]);
  const [refetch, setRefetch] = React.useState(false);

  const [notifications, setNotifications] = React.useState<
    { type: Severity; message: string }[]
  >([]);

  const notify = (type: Severity, message: string) => {
    setNotifications((prev) => [...prev, { type, message }]);
  };

  const refetchUsers = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    userApi
      .getUsers()
      .then((response) => {
        setUsers(response.data);
      })
      .catch((error) => notify("error", "Users not fetched: " + error.message));
  }, [refetch]);

  const idList = React.useMemo(
    () => selected.map((user: userType.User) => user.id || -1),
    [selected]
  );

  const selectionState = React.useMemo(() => {
    const checkOptions = (active: number) => {
      if (active === selected.length && selected.length > 0) return "true";
      else if (active === 0) return "false";
      else return "mixed";
    };

    const activeNumber = selected.filter(
      (user: userType.User) => user.is_active
    ).length;
    const staffNumber = selected.filter(
      (user: userType.User) => user.is_staff
    ).length;
    const suNumber = selected.filter(
      (user: userType.User) => user.is_superuser
    ).length;

    return {
      active: checkOptions(activeNumber),
      staff: checkOptions(staffNumber),
      su: checkOptions(suNumber),
    };
  }, [selected]);

  const handleDelete = () => {
    userApi
      .deleteUsers(idList)
      .then((response) => {
        refetchUsers();
        notify("success", "User/s deleted");
      })
      .catch((error) =>
        notify("error", "Error deleting user/s: " + error.message)
      );
  };

  const handleChangeActive = (value: boolean) => {
    notify("info", "Loading...");

    userApi
      .updateUsersActive(idList, value)
      .then((response) => {
        refetchUsers();
        notify("success", "User/s status changed");
      })
      .catch((error) =>
        notify("error", "Error updating status: " + error.message)
      );
  };
  const handleChangeRole = (value: boolean, role: "Staff" | "Superuser") => {
    notify("info", "Loading...");

    userApi
      .updateUsersRole(idList, value, role)
      .then((response) => {
        refetchUsers();
        notify("success", "User/s roles changed");
      })
      .catch((error) =>
        notify("error", "Error updating roles: " + error.message)
      );
  };

  return (
    <>
      <Page title="Users" notifications={notifications}>
        <UserTable users={users} setSelected={setSelected} />
      </Page>
      <ActionBar
        selection={selected}
        actions={[
          <UserForm
            initialUser={selected.length === 1 ? selected[0] : undefined}
            refetch={refetchUsers}
            notify={notify}
          />,
        ]}
        individualActions={[
          {
            icon: <Refresh />,
            title: "Refresh",
            onClick: () => refetchUsers(),
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
              selectionState.active === "true" ? (
                <Pause color="warning" />
              ) : (
                <PlayArrow />
              ),
            title:
              selectionState.active === "true"
                ? "Mark as Inactive"
                : "Mark as Active",
            disabled: selectionState.active === "mixed",
            onClick: () => {
              console.log("switch active");
              selectionState.active === "true"
                ? handleChangeActive(false)
                : handleChangeActive(true);
            },
          },
          {
            icon:
              selectionState.staff === "true" ? (
                <Verified color="warning" />
              ) : (
                <Verified />
              ),
            title:
              selectionState.staff === "true" ? "Remove Staff" : "Make Staff",
            disabled: selectionState.staff === "mixed",
            onClick: () => {
              console.log("switch staff");
              selectionState.staff === "true"
                ? handleChangeRole(false, "Staff")
                : handleChangeRole(true, "Staff");
            },
          },
          {
            icon:
              selectionState.su === "true" ? (
                <AdminPanelSettings color="warning" />
              ) : (
                <AdminPanelSettings />
              ),
            title:
              selectionState.su === "true"
                ? "Remove SuperUser"
                : "Make SuperUser",
            disabled: selectionState.su === "mixed",
            onClick: () => {
              console.log("switch staff");
              selectionState.su === "true"
                ? handleChangeRole(false, "Superuser")
                : handleChangeRole(true, "Superuser");
            },
          },
        ]}
      />
    </>
  );
};

export default UsersPage;
