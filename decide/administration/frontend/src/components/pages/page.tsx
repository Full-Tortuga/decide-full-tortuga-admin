import React, { ReactElement } from "react";
import { Box } from "@mui/material";

import { Title } from "components/01-atoms";

const Page = (props: {
  title: string;
  children?: ReactElement | ReactElement[] | string;
}) => {
  return (
    <>
      <Box className="inline-block w-10/12 h-screen p-1 md:p-5 xl:p-10">
        <Title title={props.title} variant="h2" />
        <Box id="content" className="m-2 inline-block w-10/12">
          {props.children}
        </Box>
      </Box>
    </>
  );
};

export default Page;
