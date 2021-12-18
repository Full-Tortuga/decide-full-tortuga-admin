import React from "react";
import { useForm, SubmitHandler } from "react-hook-form";

import { authApi } from "api";

import Page from "../page";
import { FormItem } from "components/01-atoms/Input";
import { Button } from "components/01-atoms";
import { Box } from "@mui/material";

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

  const onSubmitFailed = (e: any) => {
    if (!e.response) {
      setError("password", { type: "manual", message: "Server Error" });
      setError("username", { type: "manual", message: "" });
    }
    if (e?.response?.status === 400) {
      setError("password", {
        type: "manual",
        message: e.response.data.non_field_errors[0],
      });
      setError("username", {
        type: "manual",
      });
    }
  };

  const onSubmit: SubmitHandler<LoginInputs> = (data) => {
    console.log("Login:", data.username);
    authApi
      .login(data.username, data.password)
      .then((r) => {
        window.location.reload();
      })
      .catch((e) => {
        onSubmitFailed(e);
      });
  };

  return (
    <Page title="Log In">
      <Box className="flex flex-col w-60 mx-auto my-4">
        <form
          className="space-y-5"
          onSubmit={(e) => {
            e.preventDefault();
            onSubmit(getValues());
          }}
        >
          <FormItem.TextInput
            name="username"
            control={control}
            error={errors.username?.message}
          />
          <FormItem.SecretInput
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
