import { useRef } from "react";
import { Messages } from "primereact/messages";
import Api from "../services/backend";
import "../css/ConnectionTest.css";
import { Button } from "primereact/button";

const ConnectionTest = () => {
  const messages = useRef(null);

  function connect() {
    Api.connection_test()
      .then((status) => {
        if (status === 200) {
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
    <div>
      <Messages ref={messages}></Messages>
      <Button
        className="p-button-outlined"
        id="button-connection-test"
        onClick={connect}
      >
        Conectar con decide (prueba de conexión)
      </Button>
    </div>
  );
};

export default ConnectionTest;
