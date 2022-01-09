import React, { ReactElement } from "react";

import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Tooltip } from "@mui/material";
import { Home, Person, HowToVote, Logout } from "@mui/icons-material";
import { Link, useLocation } from "react-router-dom";

import { authApi } from "api";
import { sessionUtils } from "utils";

import { IconButton } from "components/01-atoms";

const LinkTab = (props: {
  label?: string;
  icon?: ReactElement;
  href?: string;
}) => {
  return (
    <Link to={props.href || "."}>
      <Tooltip title={props.label || ""}>
        <Tab icon={props.icon} />
      </Tooltip>
    </Link>
  );
};

const Menu = (props: { hidden: boolean }) => {
  const [value, setValue] = React.useState(0);

  const location = useLocation();

  React.useEffect(() => {
    const tab = location.pathname.split("/")[1];
    if (tab === "" || tab === "home") setValue(0);
    else if (tab === "users") setValue(1);
    else if (tab === "votings") setValue(2);
  }, [location]);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box className="inline-flex flex-col w-1/12 h-screen justify-between py-12">
      <div>
        <HowToVote scale={100} />
        <p className="text-sm font-bold">DECIDE</p>
        <p className="text-xs">ADMIN</p>
      </div>

      {!props.hidden && (
        <nav>
          <Tabs
            value={value}
            onChange={handleChange}
            aria-label="nav tabs"
            orientation="vertical"
            centered
          >
            <LinkTab label="Home" icon={<Home />} href="/home" />
            <LinkTab label="Users" icon={<Person />} href="/users" />
            <LinkTab label="Votings" icon={<HowToVote />} href="/votings" />
          </Tabs>
        </nav>
      )}
      <IconButton
        title="Logout"
        onClick={() =>
          authApi.logout().finally(() => {
            sessionUtils.removeToken();
            window.location.reload();
          })
        }
        icon={<Logout />}
      />
    </Box>
  );
};

export default Menu;
