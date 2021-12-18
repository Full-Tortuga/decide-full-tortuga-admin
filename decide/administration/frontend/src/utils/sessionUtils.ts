const sessionUtils = {
  getCsrfToken: () => {
    console.log(document.cookie);

    return document.cookie
      .split(";")
      ?.find((row) => row.startsWith("csrftoken"))
      ?.split("=")?.[1];
  },
  removeCsrfToken: () => {
    document.cookie =
      "csrftoken=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    console.log(document.cookie);
  },
};

export default sessionUtils;
