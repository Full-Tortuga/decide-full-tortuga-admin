import React from 'react';
import { checkErrors } from './Utils';

//Register Box 
class LoginLDAP extends React.Component {

    constructor(props:any) {
      super(props);
      this.state = {};
    }
  
    submitRegister(e:any) {}
  
    render() {
      return (
        <form id='ldap-form' method='POST' action='/authentication/loginLDAP/' onSubmit={checkErrors}>
        
        <div className="inner-container">
          <div className="header">
            Login LDAP
          </div>
          <div className="box">
            <div className="input-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                name="username"
                className="login-input"
                placeholder="Username"
                required/>
            </div>
  
            <div className="input-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                name="password"
                className="login-input"
                placeholder="Password"
                required/>
            </div>
            <button
              type="submit"
              className="login-btn"
              >Login with LDAP</button>
          </div>
        </div>
        </form>
      );
    }
  }
  
export default LoginLDAP;  