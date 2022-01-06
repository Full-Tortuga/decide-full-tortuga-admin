const util = () => {
  return null;
};

const parseErrors = (error: any) => {
  return error.response.data?.join(", ");
};

export { util, parseErrors };
