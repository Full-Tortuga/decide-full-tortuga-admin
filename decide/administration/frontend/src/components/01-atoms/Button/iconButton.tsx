import React, { ReactElement } from "react";

import { IconButton, Tooltip } from "@mui/material";

const Component = (props: {
  title: string;
  icon: ReactElement;
  type?: "submit" | "button" | "reset";
  disabled?: boolean;
  onClick?: () => void;
}) => {
  return (
    <Tooltip title={props.title}>
      <IconButton
        color="primary"
        type={props.type || "button"}
        onClick={props.onClick}
        disabled={props.disabled}
      >
        {props.icon}
      </IconButton>
    </Tooltip>
  );
};

export default Component;
