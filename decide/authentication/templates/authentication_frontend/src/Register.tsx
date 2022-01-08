import React from 'react';

//Register Box 
class RegisterBox extends React.Component {

    constructor(props:any) {
      super(props);
      this.state = {};
    }
  
    submitRegister(e:any) {}
  
    render() {
      return (
        <div className="inner-container">
          <div className="header">
            Register
          </div>
          <div className="box">
  
            <div className="input-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                name="username"
                className="login-input"
                placeholder="Username"/>
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
                placeholder="Password"/>
            </div>
            <div className="input-group">
              <label htmlFor="password2">Repeat Password</label>
              <input
                type="password2"
                name="password2"
                className="login-input"
                placeholder="Repeat Password"/>
            </div>
            <button
              type="button"
              className="login-btn"
              onClick={this
              .submitRegister
              .bind(this)}>Register</button>
          </div>
        </div>
      );
    }
  }
  
export default RegisterBox;  