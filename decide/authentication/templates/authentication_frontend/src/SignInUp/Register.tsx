import React from 'react';
import { checkErrors } from './Utils';

//Register Box 
class RegisterBox extends React.Component {

    constructor(props:any) {
      super(props);
      this.state = {};
    }
  
    submitRegister(e:any) {}
  
    render() {
      return (
        <form id='register-form' method='POST' action='/authentication/register_user/' onSubmit={checkErrors}>
        
        <div className="inner-container">
          <div className="header">
            Register
          </div>
          <div className="box">
            <div className="input-group">
              <label htmlFor="firstname">First Name</label>
              <input
                type="text"
                name="firstname"
                className="login-input"
                placeholder="First name"/>
            </div>
            <div className="input-group">
              <label htmlFor="lastname">Last Name</label>
              <input
                type="text"
                name="lastname"
                className="login-input"
                placeholder="Last name"/>
            </div>
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
              <label htmlFor="email">Email</label>
              <input type="text" name="email" className="login-input" placeholder="Email"/>
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
            <div className="input-group">
              <label htmlFor="password2">Repeat Password</label>
              <input
                type="password"
                name="password2"
                className="login-input"
                placeholder="Repeat Password"
                required/>
            </div>
            <button
              type="submit"
              className="login-btn"
              >Register</button>
          </div>
        </div>
        </form>
      );
    }
  }
  
export default RegisterBox;  