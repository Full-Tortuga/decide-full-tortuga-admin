import React, { ReactElement } from "react";
import {
  Box,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Typography,
} from "@mui/material";

const Circle = (
  value: number,
  icon: ReactElement,
  color: "success" | "warning" | "primary"
) => {
  return (
    <Box sx={{ position: "relative" }}>
      <CircularProgress
        variant="determinate"
        sx={{
          color: (theme) => theme.palette.grey[200],
          position: "absolute",
          left: 0,
        }}
        size={100}
        thickness={6}
        value={100}
      />
      <CircularProgress
        variant="determinate"
        disableShrink
        size={100}
        thickness={8}
        value={value || 0}
        color={color}
      />
      <span className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        {icon}
      </span>
    </Box>
  );
};

const Component = (props: {
  title: string;
  total: number;
  active: number;
  icon: ReactElement;
  color: "success" | "warning" | "primary";
}) => {
  return (
    <Card className="grid-cols-1 p-3">
      <div className="flex justify-center items-center">
        {Circle(
          Math.floor((props.active / props.total) * 100),
          props.icon,
          props.color
        )}
      </div>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {props.title}
        </Typography>
        <p>
          Total: <Chip label={props.total} color="default" />
        </p>
        <p>
          {props.title}: <Chip label={props.active} color={props.color} />
        </p>
      </CardContent>
    </Card>
  );
};

export default Component;
