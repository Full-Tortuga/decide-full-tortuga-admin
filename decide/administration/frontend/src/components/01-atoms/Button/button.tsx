import React from "react";

import { Button } from "@mui/material";

type Variant = "outlined" | "contained" | "text";

const Component = (props: {
  title: string;
  type?: "submit" | "button" | "reset";
  variant?: Variant;
  disabled?: boolean;
  onClick?: () => void;
}) => {
  return (
    <Button
      type={props.type || "button"}
      variant={props.variant || "outlined"}
      onClick={props.onClick}
      disabled={props.disabled}
    >
      {props.title}
    </Button>
  );
};

export default Component;
