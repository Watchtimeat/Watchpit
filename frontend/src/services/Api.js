import axios from "axios";
import EventBus from "./EventBus";

class Api {
  setBaseURL(url) {
    axios.defaults.baseURL = url;
  }

  setToken(token) {
    if (token)
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
  }

  getMessage(error) {
    if (error.response)
      return `[${error.response.status}] ${error.response.data.message}`;
    else return error.message;
  }

  post(url, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: url,
        method: "post",
        data: data,
        withCredentials: true,
      })
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          const message = this.getMessage(error);
          EventBus.emit("error", message);
          reject(message);
        });
    });
  }

  patch(url, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: url,
        method: "patch",
        data: data,
        withCredentials: true,
      })
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          const message = this.getMessage(error);
          EventBus.emit("error", message);
          reject(message);
        });
    });
  }

  delete(url) {
    return new Promise((resolve, reject) => {
      axios({
        url: url,
        method: "delete",
        withCredentials: true,
      })
        .then((response) => {
          resolve();
        })
        .catch((error) => {
          const message = this.getMessage(error);
          EventBus.emit("error", message);
          reject(message);
        });
    });
  }

  get(url, params) {
    if (params)
      url +=
        "?" +
        Object.keys(params)
          .map(
            (k) => encodeURIComponent(k) + "=" + encodeURIComponent(params[k])
          )
          .join("&");
    return new Promise((resolve, reject) => {
      axios({
        url: url,
        method: "get",
        withCredentials: true,
      })
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          const message = this.getMessage(error);
          EventBus.emit("error", message);
          reject(message);
        });
    });
  }
}

export default new Api();
