import React from "react";

import { FormControlLabel, FormLabel, Radio, RadioGroup } from "@mui/material";
import { Controller } from "react-hook-form";
import { RadioOption, RadioProps } from "..";

const Component = (props: RadioProps) => {
  return (
    <>
      <FormLabel>{props.name.toLowerCase()}</FormLabel>
      <Controller
        name={props.name}
        control={props.control}
        rules={props.rules}
        render={({ field, fieldState }) => (
          <RadioGroup {...field}>
            {props.options.map((option: RadioOption) => (
              <FormControlLabel
                value={option.value}
                control={<Radio />}
                label={option.label}
              />
            ))}
          </RadioGroup>
        )}
      />
    </>
  );
};

export default Component;
