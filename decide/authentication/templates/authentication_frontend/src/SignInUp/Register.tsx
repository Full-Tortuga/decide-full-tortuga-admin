import React from 'react';
import { Button, Form, FormControl, InputGroup } from 'react-bootstrap';
import { checkErrors } from './Utils';

//Register Box 
class RegisterBox extends React.Component {

  constructor(props: any) {
    super(props);
    this.state = {};
  }

  submitRegister(e: any) { }

  render() {
    return (
      <Form id='register-form' method='POST' action='/authentication/register_user/' onSubmit={checkErrors}>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            First Name
          </InputGroup.Text>
          <FormControl type="text" name="firstname"
            className="login-input" />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Last Name
          </InputGroup.Text>
          <FormControl type="text" name="lastname"
            className="login-input" />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Username
          </InputGroup.Text>
          <FormControl type="text" name="username"
            className="login-input" required={true} />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Email
          </InputGroup.Text>
          <FormControl type="email" name="email"
            className="login-input" />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Password
          </InputGroup.Text>
          <FormControl type="password" name="password"
            className="login-input" required={true} />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon3">
            Repeat password
          </InputGroup.Text>
          <FormControl type="password" name="password2"
            className="login-input" required={true} />
        </InputGroup>

        <Button
          type="submit"
          className="login-btn"
        >Register</Button>

      </Form>
    );
  }
}

export default RegisterBox;  