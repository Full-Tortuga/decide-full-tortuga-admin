import React from "react";

import { Typography } from "@mui/material";

type Variant =
  | "h1"
  | "h2"
  | "h3"
  | "h4"
  | "subtitle1"
  | "subtitle2"
  | "body1"
  | "body2"
  | "caption"
  | "button"
  | "overline";

const Component = (props: { title: string; variant: Variant }) => {
  return <Typography variant={props.variant}>{props.title}</Typography>;
};

export default Component;
