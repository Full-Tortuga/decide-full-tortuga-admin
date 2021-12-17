import "./css/App.css";
import { Card } from "@nextui-org/react";
import React from "react";
import axios from "axios";
import { useRef } from "react";
import { Messages } from "primereact/messages";

function App() {
  const messages = useRef(null);

  function connect() {
    axios
      .get("http://localhost:8000/admin/")
      .then((res) => {
        if (res.status === 200) {
          messages.current.show({
            severity: "success",
            summary: "Conexión exitosa",
          });
        }
      })
      .catch((err) => {
        messages.current.show({
          severity: "warn",
          summary: "Conexión fallida",
        });
      });
  }

  return (
    <React.Fragment>
      <Messages ref={messages}></Messages>
      <Card
        id="principal"
        color="gradient"
        textColor="white"
        width="50%"
        hoverable="true"
        onClick={connect}
        clickable="true"
      >
        Conectar con decide (prueba de conexión)
      </Card>
    </React.Fragment>
  );
}

export default App;
