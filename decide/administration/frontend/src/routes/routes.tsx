import React, { Suspense } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import { Loader } from "components/01-atoms";
import { Menu } from "components/templates";
import { NotFoundPage, UsersPage, HomePage, LoginPage } from "components/pages";
import { localStore } from "store";

export const AppRoutes = () => {
  const isAuthenticated = localStore.getToken() !== null;

  return (
    <Suspense
      fallback={
        <div className="h-full w-full flex items-center justify-center">
          <Loader />
        </div>
      }
    >
      <Router basename="/administration">
        <Menu />
        <Routes>
          {isAuthenticated ? (
            <>
              <Route path="/users" element={<UsersPage />} />
              <Route path="/home" element={<HomePage />} />
              <Route path="/404" element={<NotFoundPage />} />
              <Route path="*" element={<Navigate to="/404" />} />
            </>
          ) : (
            <Route path="*" element={<LoginPage />} />
          )}
        </Routes>
      </Router>
    </Suspense>
  );
};
