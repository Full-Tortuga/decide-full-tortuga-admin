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
  const bulkEnabled = React.useMemo(
    () => props.selection && props.selection.length >= 1,
    [props.selection]
  );

  return (
    <Box id="actions" className="inline-flex items-center w-1/12 h-screen px-2">
      <Box className="w-12 flex flex-col border rounded p-2 gap-3">
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
