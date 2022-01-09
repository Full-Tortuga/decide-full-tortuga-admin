import React from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { Box } from "@mui/material";

import { authApi } from "api";
import { sessionUtils, utils } from "utils";

import { Severity } from "components/01-atoms/Notification";
import { Input, Button } from "components/01-atoms";
import Page from "../page";

type LoginInputs = {
  username: string;
  password: string;
};

const LoginPage = () => {
  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<LoginInputs>();

  const [notifications, setNotifications] = React.useState<
    { type: Severity; message: string }[]
  >([]);

  const notify = (type: Severity, message: string) => {
    setNotifications((prev) => [...prev, { type, message }]);
  };

  const onSubmitFailed = (e: any) => {
    if (!e.response) {
      setError("password", { type: "manual", message: "Server Error" });
      setError("username", { type: "manual", message: "" });
      notify("error", "Server Error");
    }
    if (e?.response?.status === 400) {
      setError("password", {
        type: "manual",
        message: e.response.data?.password || "",
      });
      setError("username", {
        type: "manual",
        message: e.response.data?.username || "",
      });
      notify(
        "error",
        "ERRORS: " + utils.parseErrors(e) ||
          e.response.data.non_field_errors[0] ||
          "Unknown error"
      );
    }
  };

  const onSubmit: SubmitHandler<LoginInputs> = (data) => {
    authApi
      .login(data.username, data.password)
      .then((r) => {
        sessionUtils.setToken(r?.headers["set-cookie"]?.[0]);
        window.location.reload();
      })
      .catch((e) => {
        onSubmitFailed(e);
      });
  };

  return (
    <Page title="Log In" notifications={notifications}>
      <Box className="flex flex-col w-60 mx-auto my-4">
        <form
          className="space-y-5"
          onSubmit={(e) => {
            e.preventDefault();
            onSubmit(getValues());
          }}
        >
          <Input.Text
            name="username"
            control={control}
            error={errors.username?.message}
          />
          <Input.Secret
            name="password"
            control={control}
            error={errors.password?.message}
          />
          <Button title="LogIn" type="submit" />
        </form>
      </Box>
    </Page>
  );
};

export default LoginPage;
