import React from "react";
import { useForm, SubmitHandler } from "react-hook-form";

import { localStore } from "store";
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
    formState: { errors },
  } = useForm<LoginInputs>();

  const onSubmit: SubmitHandler<LoginInputs> = (data) => {
    console.log("Login:", data.username);
    authApi.login(data.username, data.password).then((r) => {
      localStore.setToken(r.data);
      window.location.reload();
    });
  };

  return (
    <Page title="Log In">
      <Box className="flex flex-col w-60 mx-auto my-4">
        <form
          className="space-y-10"
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
