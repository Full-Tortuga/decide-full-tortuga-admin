import React, { ReactElement } from "react";

import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Link, Outlet } from "react-router-dom";
import { Tooltip } from "@mui/material";
import { Error, Home, HomeMaxSharp, Person } from "@mui/icons-material";

const LinkTab = (props: {
  label?: string;
  icon?: ReactElement;
  href?: string;
}) => {
  return (
    <Link to={props.href || "."}>
      <Tooltip title={props.label || ""}>
        <Tab {...props} />
      </Tooltip>
    </Link>
  );
};

const Menu = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box>
      <nav>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="nav tabs"
          centered
        >
          <LinkTab label="Home" icon={<Home />} href="/home" />
          <LinkTab label="Users" icon={<Person />} href="/users" />
          <LinkTab label="NotFound" icon={<Error />} href="/404" />
        </Tabs>
      </nav>
      <Outlet />
    </Box>
  );
};

export default Menu;
