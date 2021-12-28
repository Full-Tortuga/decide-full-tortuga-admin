import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { userType } from "types";
import { ModalPage, Modal } from "components/02-molecules";
import { Add, Edit } from "@mui/icons-material";
import { FormItem } from "components/01-atoms/Input";
import { userApi } from "api";
import { utils } from "utils";

const Component = (props: {
  initialUser?: userType.User;
  refetch: () => void;
}) => {
  const editMode = React.useMemo(
    () => !!props.initialUser?.id,
    [props.initialUser]
  );

  const {
    control,
    getValues,
    trigger,
    setError,
    clearErrors,
    formState: { errors },
    reset,
  } = useForm<userType.UserFormFields>({ mode: "onChange" });

  const [sent, setSent] = React.useState(false);

  React.useEffect(() => {
    reset({});
    clearErrors();
    trigger();
    control._defaultValues = {
      username: props.initialUser?.username,
      password: "",
      first_name: props.initialUser?.first_name,
      last_name: props.initialUser?.last_name,
      email: props.initialUser?.email,
    };
  }, [props.initialUser, control, reset, clearErrors, trigger]);

  const onSubmitFailed = (e: any) => {
    clearErrors();
    setError("username", { type: "manual", message: e });
  };

  const onSubmitSuccess = () => {
    setSent(!sent);
    props.refetch();
    reset({});
  };

  const onSubmit: SubmitHandler<userType.UserFormFields> = (data) => {
    console.log("submit:", data);

    if (Object.keys(errors).length === 0)
      if (editMode && props.initialUser?.id) {
        userApi
          .updateUser(props.initialUser?.id, data)
          .then(() => onSubmitSuccess())
          .catch((error) => onSubmitFailed(utils.parseErrors(error)));
      } else {
        userApi
          .createUser(data)
          .then(() => onSubmitSuccess())
          .catch((error) => onSubmitFailed(utils.parseErrors(error)));
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
            rules={{
              required: "This field is required",
              pattern: {
                value: /^[a-z0-9]+$/,
                message: "Use lowercase letters and numbers",
              },
            }}
          />
          <FormItem.SecretInput
            control={control}
            name="password"
            rules={editMode ? {} : { required: "This field is required" }}
          />
          <FormItem.TextInput control={control} name="first_name" />
          <FormItem.TextInput control={control} name="last_name" />
          <FormItem.TextInput
            control={control}
            name="email"
            rules={{
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: "Invalid email address",
              },
            }}
          />
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
