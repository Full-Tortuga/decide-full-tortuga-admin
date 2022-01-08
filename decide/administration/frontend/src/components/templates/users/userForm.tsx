import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { Add, Edit } from "@mui/icons-material";

import { userApi } from "api";
import { utils } from "utils";
import { userType } from "types";

import { Input } from "components/01-atoms";
import { Severity } from "components/01-atoms/Notification";
import { ModalPage, Modal } from "components/02-molecules";

const Component = (props: {
  initialUser?: userType.User;
  refetch: () => void;
  notify?: (type: Severity, message: string) => void;
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
    props.notify?.("error", "Submit failed: " + e);
  };

  const onSubmitSuccess = () => {
    setSent(!sent);
    props.refetch();
    props.notify?.("success", editMode ? "User updated" : "User created");
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
          <Input.Text
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
          <Input.Secret
            control={control}
            name="password"
            rules={editMode ? {} : { required: "This field is required" }}
          />
          <Input.Text control={control} name="first_name" />
          <Input.Text control={control} name="last_name" />
          <Input.Text
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
