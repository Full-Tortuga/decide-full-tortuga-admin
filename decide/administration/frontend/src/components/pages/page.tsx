import React, { ReactElement } from "react";
import { Box } from "@mui/material";

import { Title } from "components/01-atoms";

const Page = (props: {
  title: string;
  children?: ReactElement | ReactElement[] | string;
}) => {
  return (
    <Box className="m-10 justify-center">
      <Title title={props.title} variant="h1" />

      <Box id="content" className="m-2 inline-block w-10/12">
        {props.children}
      </Box>
      <Box id="actions" className="m-2 inline-block w-2/12"></Box>
    </Box>
  );
};

export default Page;
