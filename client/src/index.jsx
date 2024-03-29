import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./styles.css";

import Protected from "./routes/Protected";
import Login from "./routes/Login";
import Register from "./routes/Register";
import Dashboard from "./routes/Dashboard";


const router = createBrowserRouter([
  {
    path:"/",
    element: <Protected />,
    children: [
      {
        path: "/",
        element: <Dashboard />
      },
    ]
  },
  {
    path: "/login",
    element: <Login />
  },
  {
    path: "/register",
    element: <Register />
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={ router } />
  </React.StrictMode>,
)
