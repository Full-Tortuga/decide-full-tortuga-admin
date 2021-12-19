import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { userType } from "types";
import { ModalPage, Modal } from "components/02-molecules";
import { Add, Edit } from "@mui/icons-material";
import { FormItem } from "components/01-atoms/Input";

const Component = (props: { initialUser?: userType.User }) => {
  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<{ username: string; username2: string }>({
    defaultValues: { username: props.initialUser?.first_name || "" },
  });

  const [sent, setSent] = React.useState(false);

  const onSubmitFailed = (e: any) => {
    console.log("error", e);
    setError("username", { type: "manual", message: "Fake Error" });
  };

  const onSubmit: SubmitHandler<{ username: string; username2: string }> = (
    data
  ) => {
    //todo: if initialUser empty then call create new user
    //todo: if initialUser is not empty, then call update
    console.log("submit:", data);
    //Todo: call api and create user,
    //Todo: if created then close modal if not, call onSubmitFailed
    setSent(true);

    onSubmitFailed("not failed");
  };

  return (
    <Modal
      onSubmit={() => onSubmit(getValues())}
      title="New User"
      openerIcon={props.initialUser ? <Edit /> : <Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información del Usuario">
          <FormItem.TextInput
            control={control}
            name="username"
            error={errors.username?.message}
          />
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
