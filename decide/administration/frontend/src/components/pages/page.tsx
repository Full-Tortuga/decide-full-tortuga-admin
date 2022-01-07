import React, { ReactElement } from "react";
import { Box } from "@mui/material";

import { Notification, Title } from "components/01-atoms";
import { Severity } from "components/01-atoms/Notification";

const Page = (props: {
  title: string;
  children?: ReactElement | ReactElement[] | string;
  notifications?: { type: Severity; message: string }[];
}) => {
  return (
    <>
      <Box className="inline-block w-10/12 h-screen p-1 md:p-5 xl:p-10">
        <Box id="content" className="my-2 ml-10 inline-block w-11/12">
          <Title title={props.title} variant="h3" />
          <hr className="my-6" />
          {props.children}
        </Box>
        <div id="Notifications">
          {props.notifications?.map((notification) => (
            <Notification
              severity={notification.type}
              message={notification.message}
            />
          ))}
        </div>
      </Box>
    </>
  );
};

export default Page;
