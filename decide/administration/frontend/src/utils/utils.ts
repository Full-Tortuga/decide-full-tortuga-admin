import { votingType } from "types";

const util = () => {
  return null;
};

const parseErrors = (error: any) => {
  return error.response.data?.join(", ");
};

const getStatus = (voting: votingType.Voting) => {
    if (voting.start_date.length > 0 && voting.end_date.length > 0) return "Finished";
    else if (voting.start_date.length > 0 && voting.end_date.length === 0) return "In progress";
    else if (voting.start_date.length === 0 && voting.end_date.length === 0) return "New";
};

export { util, parseErrors, getStatus };
