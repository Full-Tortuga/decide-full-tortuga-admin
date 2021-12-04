import React from "react";

import { FieldProps } from "..";
import ControlledInput from "../controlledInput";

const Component = (props: FieldProps) => {
  return <ControlledInput {...props} type="password" />;
};

export default Component;
