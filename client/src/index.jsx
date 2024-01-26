import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

import Login from "./routes/Login";
import Register from "./routes/Register";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Login />
  </React.StrictMode>,
)
