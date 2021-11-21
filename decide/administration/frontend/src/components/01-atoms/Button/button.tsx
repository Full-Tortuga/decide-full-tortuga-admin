import React from "react";

import { Button } from "@mui/material";

type Variant = "outlined" | "contained" | "text";

const Component = (props: { title: string; variant: Variant }) => {
  return <Button variant="outlined">{props.title}</Button>;
};

export default Component;
