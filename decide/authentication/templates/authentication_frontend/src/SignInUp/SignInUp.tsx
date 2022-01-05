import React from "react";
import "./index.css";
import LoginBox from "./Login";
import LoginLDAP from "./LoginLDAP";
import RegisterBox from "./Register";

class SignInUp extends React.Component<any,State>{

  constructor(props:any) {
    super(props);
    this.state = {
      isLoginOpen: true,
      isRegisterOpen: false,
      isLoginLDAPOpen: false,
    };
  }

  showLoginBox() {
    this.setState({isLoginOpen: true, isRegisterOpen: false, isLoginLDAPOpen: false});
  }

  showRegisterBox() {
    this.setState({isRegisterOpen: true, isLoginOpen: false, isLoginLDAPOpen: false});
  }

  showLoginLDAP() {
    this.setState({isRegisterOpen: false, isLoginOpen: false, isLoginLDAPOpen: true});
  }

  render (){
    console.log(this.state)
    return (
      <div className="root-container">
        <div id="error-box">
          <span id="error-msg"> </span>
        </div>

        <div className="box-container">
          {this.state.isLoginOpen && <LoginBox/>}
          {this.state.isRegisterOpen && <RegisterBox/>}
          {this.state.isLoginLDAPOpen && <LoginLDAP/>}
        </div>

  
        <div className="box-controller">
          <div
            className={"controller " + (this.state.isLoginOpen
            ? "selected-controller"
            : "")}
            onClick={this
            .showLoginBox
            .bind(this)}>
            Login
          </div>
          <div
            className={"controller " + (this.state.isLoginLDAPOpen
            ? "selected-controller"
            : "")}
            onClick={this
            .showLoginLDAP
            .bind(this)}>
            LDAP
          </div>
          <div
            className={"controller " + (this.state.isRegisterOpen
            ? "selected-controller"
            : "")}
            onClick={this
            .showRegisterBox
            .bind(this)}>
            Register
          </div>
        </div>
      </div>
    );
  }
  
}

interface State{
  isRegisterOpen: boolean,
  isLoginOpen: boolean
  isLoginLDAPOpen: boolean
}
export default SignInUp;
