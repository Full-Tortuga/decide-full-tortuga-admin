import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { userType } from "types";
import { ModalPage, Modal } from "components/02-molecules";
import { Add } from "@mui/icons-material";
import { FormItem } from "components/01-atoms/Input";

const Component = (props: { initialUser?: userType.User[] }) => {
  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<{ username: string; username2: string }>();

  const [sent, setSent] = React.useState(false);

  const onSubmitFailed = (e: any) => {
    console.log("error", e);
    setError("username", { type: "manual", message: "Fake Error" });
  };

  const onSubmit: SubmitHandler<{ username: string; username2: string }> = (
    data
  ) => {
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
      openerIcon={<Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información del Usuario">
          <FormItem.TextInput
            control={control}
            name="username"
            error={errors.username?.message}
          ></FormItem.TextInput>
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
