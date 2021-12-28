export type Question = {
  desc: string;
  options: { number: number; option: string }[];
};

export type Voting = {
  id?: number;
  name: string;
  desc: string;
  start_date: string;
  end_date: string;
};

export type VotingFormFields = {
  name: string;
  desc: string;
  question: Question;
  census: number[];
  auth: string;
};
