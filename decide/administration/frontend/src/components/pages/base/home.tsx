import { authApi } from "api";
import { Button } from "components/01-atoms";
import React from "react";
import { sessionUtils } from "utils";

import Page from "../page";

const HomePage = () => {
  return (
    <Page title="Home">
      <Button
        title="Logout"
        onClick={() =>
          authApi.logout().finally(() => {
            sessionUtils.removeCsrfToken();
            window.location.reload();
          })
        }
      />
    </Page>
  );
};

export default HomePage;
