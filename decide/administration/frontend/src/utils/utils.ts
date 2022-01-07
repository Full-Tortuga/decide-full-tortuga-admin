import { votingType } from "types";

const util = () => {
  return null;
};

const parseErrors = (error: any) => {
  return (
    JSON.stringify(error.response?.data)
      .replaceAll("[", "")
      .replaceAll("]", "")
      .replaceAll('"', "")
      .replaceAll("{", "")
      .replaceAll("}", "")
      .replaceAll(",", "\n") || error.message
  );
};

const getStatus = (voting: votingType.Voting) => {
  if (voting.start_date === null && voting.end_date === null) return "New";
  else if (voting.start_date.length > 0 && voting.end_date === null)
    return "In progress";
  else if (voting.start_date.length > 0 && voting.end_date.length > 0)
    return "Finished";
};

const getStatusColor = (status: string) => {
  switch (status) {
    case "New":
      return "primary";
    case "In progress":
      return "warning";
    case "Finished":
      return "success";
    default:
      return "primary";
  }
};

export { util, parseErrors, getStatus, getStatusColor };
