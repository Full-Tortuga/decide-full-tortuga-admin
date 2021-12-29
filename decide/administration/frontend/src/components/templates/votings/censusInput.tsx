import React from "react";
import { Controller } from "react-hook-form";
import { Refresh } from "@mui/icons-material";
import { FormLabel } from "@mui/material";

import { userApi } from "api";
import { userType } from "types";

import { IconButton } from "components/01-atoms";
import { UserTable } from "..";

const Component = (props: { control: any }) => {
  const [refetch, setRefetch] = React.useState(false);
  const [users, setUsers] = React.useState<userType.User[]>([]);

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

  return (
    <Controller
      name="census"
      control={props.control}
      render={({ field, fieldState }) => (
        <>
          <FormLabel>{"Census".toLowerCase()}</FormLabel>
          <UserTable
            setSelected={(selection: userType.User[]) =>
              field.onChange(selection.map((u) => u.id))
            }
            users={users}
          />
          <IconButton
            onClick={refetchUsers}
            icon={<Refresh />}
            title="Refetch"
          />
        </>
      )}
    />
  );
};

export default Component;
