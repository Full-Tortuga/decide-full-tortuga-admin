import React, { ReactElement } from "react";

import { DialogContent, DialogContentText } from "@mui/material";

const Component = (props: { description?: string; children: ReactElement }) => {
  return (
    <>
      <DialogContent>
        <DialogContentText>{props.description}</DialogContentText>
        <br />
        <div className="flex flex-col items-center">{props.children}</div>
      </DialogContent>
    </>
  );
};

export default Component;
