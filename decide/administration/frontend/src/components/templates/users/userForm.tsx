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
  const editMode = React.useMemo(
    () => !!props.initialUser,
    [props.initialUser]
  );

  const {
    control,
    getValues,
    setError,
    formState: { errors },
    reset,
  } = useForm<userType.UserFormFields>();

  const [sent, setSent] = React.useState(false);

  React.useEffect(() => {
    control._defaultValues = {
      username: props.initialUser?.username,
      password: props.initialUser?.password,
      first_name: props.initialUser?.first_name,
      last_name: props.initialUser?.last_name,
      email: props.initialUser?.email,
    };
  }, [props.initialUser, control]);

  const onSubmitFailed = (e: any) => {
    console.log("error", e);
    setError("username", { type: "manual", message: "" });
    setError("password", { type: "manual", message: "" });
    setError("first_name", { type: "manual", message: "" });
    setError("last_name", { type: "manual", message: "" });
    setError("email", { type: "manual", message: e.message });
  };

  const onSubmitSuccess = () => {
    reset({});
    setSent(!sent);
    props.refetch();
  };

  const onSubmit: SubmitHandler<userType.UserFormFields> = (data) => {
    console.log("submit:", data);

    if (editMode) {
      userApi
        .updateUser({ id: props.initialUser?.id, ...data })
        .then(() => onSubmitSuccess())
        .catch((e) => onSubmitFailed(e));
    } else {
      userApi
        .createUser(data)
        .then(() => onSubmitSuccess())
        .catch((error) => onSubmitFailed(error.message));
    }
  };

  return (
    <Modal
      onSubmit={() => onSubmit(getValues())}
      title={editMode ? "Edit " + props.initialUser?.first_name : "New User"}
      openerIcon={editMode ? <Edit /> : <Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información del Usuario">
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
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
