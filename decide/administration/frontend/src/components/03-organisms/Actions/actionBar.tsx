import React, { ReactElement } from "react";

import { Box } from "@mui/system";
import { Divider } from "@mui/material";
import { IconButton } from "components/01-atoms";

type Action = {
  title: string;
  icon: ReactElement;
  disabled?: boolean;
  onClick?: () => void;
};

const Component = (props: {
  selection?: any[];
  actions?: ReactElement[];
  individualActions?: Action[];
  bulkActions?: Action[];
}) => {
  const individualEnabled = React.useMemo(
    () => props.selection && props.selection?.length === 1,
    [props.selection]
  );
  const bulkEnabled = React.useMemo(
    () => props.selection && props.selection.length >= 1,
    [props.selection]
  );

  return (
    <Box
      id="actions"
      className="inline-block w-1/12 h-screen py-1 md:py-5 xl:py-32 px-2"
    >
      <Box className="h-full w-12 flex flex-col border rounded p-2 gap-3">
        {props.actions}
        <Divider />
        {props.individualActions?.map((action, index) => (
          <IconButton
            key={index}
            title={action.title}
            icon={action.icon}
            onClick={action.onClick}
          />
        ))}
        <Divider />
        {props.bulkActions?.map((action, index) => (
          <IconButton
            key={index}
            title={action.title}
            icon={action.icon}
            onClick={action.onClick}
            disabled={action.disabled || !bulkEnabled}
          />
        ))}
      </Box>
    </Box>
  );
};

export default Component;
