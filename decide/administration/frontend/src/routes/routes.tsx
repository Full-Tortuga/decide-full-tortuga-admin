import React, { Suspense } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import { Loader } from "../components/01-atoms";
import { NotFoundPage, UsersPage, HomePage } from "../components/pages";

import Menu from "../components/templates/menu";

export const AppRoutes = () => {
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
          <Route path="/users" element={<UsersPage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/404" element={<NotFoundPage />} />
          <Route path="*" element={<Navigate to="/home" />} />
        </Routes>
      </Router>
    </Suspense>
  );
};
