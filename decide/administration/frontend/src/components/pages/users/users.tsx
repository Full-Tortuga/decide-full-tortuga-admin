import React from "react";
import {
  AdminPanelSettings,
  Delete,
  Pause,
  PlayArrow,
  Verified,
} from "@mui/icons-material";

import { userApi } from "api";
import { userType } from "types";

import { ActionBar } from "components/03-organisms";
import { NewUserForm, UserTable } from "components/templates/users";

import Page from "../page";

const UsersPage = () => {
  const [users, setUsers] = React.useState<userType.User[]>([]);
  const [selected, setSelected] = React.useState([]);
  const [refetch, setRefetch] = React.useState(false);

  const refetchUsers = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    userApi
      .getUsers()
      .then((response) => {
        console.log(response);
        setUsers(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [refetch]);

  const idList = React.useMemo(
    () => selected.map((user: userType.User) => user.id),
    [selected]
  );

  const selectionState = React.useMemo(() => {
    const checkOptions = (active: number) => {
      if (active === selected.length) return "true";
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
    userApi.deleteUsers(idList).then((response) => {
      console.log(response);
      refetchUsers();
    });
  };

  const handleChangeActive = (value: boolean) => {
    userApi.updateUsersActive(idList, value).then((response) => {
      console.log(response);
      refetchUsers();
    });
  };
  const handleChangeRole = (value: boolean, role: "Staff" | "Superuser") => {
    userApi.updateUsersRole(idList, value, role).then((response) => {
      console.log(response);
      refetchUsers();
    });
  };

  return (
    <>
      <Page title="Users">
        <UserTable users={users} setSelected={setSelected} />
      </Page>
      <ActionBar
        selection={selected}
        actions={[
          <NewUserForm
            initialUser={selected.length === 1 ? selected[0] : undefined}
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
          {
            icon: selectionState.active === "true" ? <Pause /> : <PlayArrow />,
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
            icon: selectionState.staff === "true" ? <Pause /> : <Verified />,
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
              selectionState.su === "true" ? <Pause /> : <AdminPanelSettings />,
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
