import React, { ReactElement } from "react";

import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Tooltip } from "@mui/material";
import { Home, Person, HowToVote} from "@mui/icons-material";
import { Link } from "react-router-dom";

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

const Menu = (props: { hidden: boolean }) => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box className="inline-flex flex-col w-1/12 h-screen justify-center">
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
            <LinkTab label="Votations" icon={<HowToVote/>} href="/votations" />

          </Tabs>
        </nav>
      )}
    </Box>
  );
};

export default Menu;
