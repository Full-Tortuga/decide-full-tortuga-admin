import React, { ReactElement } from "react";

import { Dialog, DialogActions, DialogTitle } from "@mui/material";

import { Button, IconButton } from "components/01-atoms";

const Component = (props: {
  title: string;
  openerIcon: ReactElement;
  pages: ReactElement[];
  externalClose?: boolean;
  onSubmit: () => void;
}) => {
  const [open, setOpen] = React.useState(false);
  const [page, setPage] = React.useState(1);

  const handleBack = () => {
    setPage(page - 1);
  };
  const handleNext = () => {
    setPage(page + 1);
  };

  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  React.useEffect(() => {
    if (props.externalClose) handleClose();
  }, [props.externalClose]);

  return (
    <>
      <IconButton
        title={props.title}
        onClick={handleOpen}
        icon={props.openerIcon}
      />
      <Dialog open={open} onClose={handleClose} fullWidth>
        <DialogTitle>{props.title}</DialogTitle>
        <form
          className="space-y-5"
          onSubmit={(e) => {
            e.preventDefault();
            props.onSubmit();
          }}
        >
          {props.pages.map((p, i) => (
            <div hidden={page !== i + 1} key={i}>
              {p}
            </div>
          ))}
          <DialogActions className="gap-11">
            {props.pages.length > 1 && (
              <div className="flex items-end gap-5">
                <Button
                  onClick={handleBack}
                  title="Back"
                  disabled={page === 1}
                />
                {page} / {props.pages.length}
                <Button
                  onClick={handleNext}
                  title="Next"
                  disabled={page === props.pages.length}
                />
              </div>
            )}

            <Button onClick={props.onSubmit} title="Submit" type="submit" />
          </DialogActions>
        </form>
      </Dialog>
    </>
  );
};

export default Component;
