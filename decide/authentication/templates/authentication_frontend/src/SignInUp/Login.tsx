import React from 'react';
import { Button, Form, FormControl, InputGroup } from 'react-bootstrap';
import { getCookie } from './Utils';

//Login Box
class LoginBox extends React.Component {

  constructor(props: any) {
    super(props);
    this.state = {};
  }

  submitLogin(e: any) {
    e.preventDefault()
    console.log(e.target[1].value)

  }

  render() {
    const csrfToken = getCookie('csrftoken') || ''
    console.log(csrfToken)
    return (
      <Form method='POST' action='/authentication/login_form/'>
        <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

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
        >Login</Button>

      </Form>

    );
  }

}

export default LoginBox;