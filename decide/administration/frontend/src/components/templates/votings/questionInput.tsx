import React from "react";
import { Controller } from "react-hook-form";
import { Add, Remove } from "@mui/icons-material";
import { FormLabel, TextField } from "@mui/material";

import { votingType } from "types";

import { IconButton } from "components/01-atoms";

const Component = (props: { control: any }) => {
  const [value, setValue] = React.useState<votingType.Question>({
    desc: "",
    options: [
      { number: 1, option: "" },
      { number: 2, option: "" },
    ],
  });

  const handleInitialValue = (field: { onChange: any; value: any }) => {
    if (field.value) setValue(field.value);
    else field.onChange(value);
  };

  const updateDesc = (e: any) => {
    const newValue = { ...value, desc: e.target.value };
    setValue(newValue);
    return newValue;
  };

  const addOption = () => {
    const newValue = {
      ...value,
      options: [
        ...value.options,
        { number: value.options.length + 1, option: "" },
      ],
    };
    setValue(newValue);
    return newValue;
  };

  const updateOption = (number: number, option: string) => {
    const newValue = {
      ...value,
      options: value.options.map((o, i) =>
        o.number === number ? { ...o, option } : o
      ),
    };
    setValue(newValue);
    return newValue;
  };

  const removeOption = (number: number) => {
    const newValue = {
      ...value,
      options: value.options.filter((o) => o.number !== number),
    };
    setValue(newValue);
    return newValue;
  };

  return (
    <>
      <Controller
        name="question"
        control={props.control}
        rules={{
          validate: {
            descRequired: (v: votingType.Question) => !!v.desc && v.desc !== "",
            optionsRequired: (v: votingType.Question) =>
              !!v.options && v.options.length > 1,
          },
        }}
        render={({ field, fieldState }) => {
          handleInitialValue(field);
          return (
            <>
              <FormLabel>{"Question".toLowerCase()}</FormLabel>
              <TextField
                autoComplete="off"
                onChange={(e) => field.onChange(updateDesc(e))}
                type="text"
                label="question"
                required
                error={fieldState.invalid}
                helperText={fieldState.error?.message}
                value={field.value?.desc || ""}
              />
              <FormLabel className="mt-10">{"Options".toLowerCase()}</FormLabel>
              {(field.value as votingType.Question)?.options.map((o, i) => (
                <div className="flex flex-row items-center">
                  <TextField
                    key={i}
                    autoComplete="off"
                    onChange={(e) =>
                      field.onChange(updateOption(o.number, e.target.value))
                    }
                    value={field.value?.options?.[i]?.option || ""}
                    type="text"
                    label={`option ${o.number}`}
                    required
                    error={fieldState.invalid}
                    helperText={fieldState.error?.message}
                  />
                  {i > 1 && (
                    <IconButton
                      onClick={() => field.onChange(removeOption(o.number))}
                      icon={<Remove />}
                      title="Remove Option"
                    />
                  )}
                </div>
              ))}
              <hr />
              <IconButton
                onClick={() => field.onChange(addOption())}
                icon={<Add />}
                title="Add Option"
              />
            </>
          );
        }}
      />
    </>
  );
};

export default Component;
