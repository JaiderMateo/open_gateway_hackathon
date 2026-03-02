import React from "react";
import ReactDOM from "react-dom/client";
import { PresenceCheck } from "./components/PresenceCheck";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <PresenceCheck />
  </React.StrictMode>
);
