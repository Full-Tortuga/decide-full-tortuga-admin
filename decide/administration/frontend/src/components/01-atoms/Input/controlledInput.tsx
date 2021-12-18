import React from "react";

import { FormLabel, TextField } from "@mui/material";
import { Controller } from "react-hook-form";
import { InputProps } from ".";

const ControlledInput = (props: InputProps) => {
  return (
    <Controller
      name={props.name}
      control={props.control}
      render={({ field: { onChange, value } }) => (
        <div>
          {props.useFormLabel && (
            <FormLabel>{props.name.toUpperCase()}</FormLabel>
          )}
          <TextField
            type={props.type}
            name={props.name}
            label={props.name}
            value={value}
            onChange={onChange}
            error={props.error !== undefined}
          />
        </div>
      )}
    />
  );
};

export default ControlledInput;
