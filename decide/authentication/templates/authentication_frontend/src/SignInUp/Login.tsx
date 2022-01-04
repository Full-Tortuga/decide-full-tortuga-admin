import React from 'react';
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
      <form method='POST' action='/authentication/login_form/'>
        <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken}/> 
        <div className="inner-container">
          <div className="header">
            Login
          </div>
          <div className="box">

            <div className="input-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                name="username"
                className="login-input"
                placeholder="Username" required/>
            </div>

            <div className="input-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                name="password"
                className="login-input"
                placeholder="Password" required/>
            </div>

            <button
              type="submit"
              className="login-btn"
              >Login</button>
          </div>
        </div>

      </form>

    );
  }

}

export default LoginBox;