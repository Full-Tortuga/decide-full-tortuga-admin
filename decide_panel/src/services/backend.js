import axios from "axios";

const REACT_APP_URI_BACKEND = process.env.REACT_APP_URI_BACKEND;

const Api = {
  connection_test() {
    return axios
      .get(REACT_APP_URI_BACKEND + "admin/")
      .then((res) => res.status);
  },

  get_census(voting_id) {
    return axios
      .get(REACT_APP_URI_BACKEND + "census/" + voting_id + "/")
      .then((res) => res.data);
  },

  get_votes() {
    return axios
      .get(REACT_APP_URI_BACKEND + "voting/list")
      .then((res) => res.data);
  },

  create_backup() {
    return axios
      .post(REACT_APP_URI_BACKEND + "backups/create")
      .then((res) => res.status);
  },

  get_backups() {
    return axios
      .get(REACT_APP_URI_BACKEND + "backups/list")
      .then((res) => res.data);
  },

  restore_backup(backup) {
    return axios
      .post(REACT_APP_URI_BACKEND + "backups/restore/" + backup)
      .then((res) => res.status);
  },

  get_votes_chart(voting_id) {
    return axios
      .get(REACT_APP_URI_BACKEND + "voting/?id=" + voting_id)
      .then((res) => res.data);
  },
};

export default Api;
