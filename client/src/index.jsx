import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { authLoader, logoutUser } from "./routes/loaders/auth";
import spotifyAuthLoader from "./routes/loaders/spotifyAuth";

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
    ],
    loader: authLoader
  },
  {
    path: "/register",
    element: <Register />
  },
  {
    path: "/login",
    element: <Login />,
    loader: authLoader
  },
  {
    path: "/login/auth/false",
    element: <Login />,
    loader: () => (false)
  },
  {
    path: "/logout",
    loader: logoutUser
  },
  {
    // User is redirected to this path after giving Spotify oAuth access
    path: "/auth/spotify/tokens",
    loader: spotifyAuthLoader
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={ router } />
  </React.StrictMode>,
)
