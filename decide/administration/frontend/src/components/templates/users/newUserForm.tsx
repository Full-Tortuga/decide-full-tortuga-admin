import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { userType } from "types";
import { ModalPage, Modal } from "components/02-molecules";
import { Add, Edit } from "@mui/icons-material";
import { FormItem } from "components/01-atoms/Input";
import { userApi } from "api";

const Component = (props: {
  initialUser?: userType.User;
  refetch: () => void;
}) => {
  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<{
    username: string;
    password: string;
    first_name: string;
    last_name: string;
    email: string;
  }>({
    defaultValues: {
      username: props.initialUser?.username || "",
      password: props.initialUser?.password || "",
      first_name: props.initialUser?.first_name || "",
      last_name: props.initialUser?.last_name || "",
      email: props.initialUser?.email || "",
    },
  });

  const [sent, setSent] = React.useState(false);

  const onSubmitFailed = (e: any) => {
    console.log("error", e);
    setError("username", { type: "manual", message: "Fake Error" });
    setError("password", { type: "manual", message: "Fake Error2" });
    setError("first_name", { type: "manual", message: "Fake Error2" });
    setError("last_name", { type: "manual", message: "Fake Error2" });
    setError("email", { type: "manual", message: "Error in email" });
  };

  const onSubmit: SubmitHandler<{
    username: string;
    password: string;
    first_name: string;
    last_name: string;
    email: string;
  }> = (data) => {
    //todo: if initialUser empty then call create new user
    //if (props.initialUser?.first_name)
    //todo: if initialUser is not empty, then call update
    console.log("submit:", data);
    //Todo: call api and create user,
    //Todo: if created then close modal if not, call onSubmitFailed
    userApi
      .createUser(data)
      .then((response) => {
        setSent(true);
        props.refetch();
      })
      .catch((error) => onSubmitFailed(error.message));
  };

  return (
    <Modal
      onSubmit={() => onSubmit(getValues())}
      title="New User"
      openerIcon={props.initialUser ? <Edit /> : <Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información del Usuario">
          <>
            <FormItem.TextInput
              control={control}
              name="username"
              error={errors.username?.message}
            />
            <FormItem.SecretInput
              control={control}
              name="password"
              error={errors.password?.message}
            />
            <FormItem.TextInput
              control={control}
              name="first_name"
              error={errors.first_name?.message}
            />
            <FormItem.TextInput
              control={control}
              name="last_name"
              error={errors.last_name?.message}
            />
            <FormItem.TextInput
              control={control}
              name="email"
              error={errors.email?.message}
            />
          </>
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
