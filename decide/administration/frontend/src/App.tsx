import React, { useEffect } from "react";

import { AppRoutes } from "routes";
import { localStore } from "store";

import "App.css";
import { authApi } from "api";

const App = () => {
  useEffect(() => {
    return () => {
      localStore.clearToken();
    };
  }, []);
  return (
    <div className="App">
      <AppRoutes />
    </div>
  );
};

export default App;
