import React from "react";
import { Button, Form, FormControl, InputGroup } from "react-bootstrap";
import { checkErrors } from "./Utils";

//Register Box 
class LoginLDAP extends React.Component {

  constructor(props: any) {
    super(props);
    this.state = {};
  }

  submitRegister(e: any) { }

  render() {
    return (
      <Form id='ldap-form' method='POST' action='/authentication/loginLDAP/' onSubmit={checkErrors}>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Username
          </InputGroup.Text>
          <FormControl type="text" name="username"
            className="login-input" required={true} />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Password
          </InputGroup.Text>
          <FormControl type="password" name="password"
            className="login-input" required={true} />
        </InputGroup>

        <Button
          type="submit"
          className="login-btn"
        >Login with LDAP</Button>

      </Form>
    );
  }
}

export default LoginLDAP;  