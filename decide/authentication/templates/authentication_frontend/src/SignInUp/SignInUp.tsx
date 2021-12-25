import React from 'react';
import './index.css';
import LoginBox from './Login';
import RegisterBox from './Register';

class SignInUp extends React.Component<any,State>{

  constructor(props:any) {
    super(props);
    this.state = {
      isLoginOpen: true,
      isRegisterOpen: false
    };
  }

  showLoginBox() {
    this.setState({isLoginOpen: true, isRegisterOpen: false});
  }

  showRegisterBox() {
    this.setState({isRegisterOpen: true, isLoginOpen: false});
  }

  render (){
    console.log(this.state)
    return (
      <div className="root-container">
        <div className="error-box active">
          <span id="error-msg"> </span>
        </div>

        <div className="box-container">
          {this.state.isLoginOpen && <LoginBox/>}
          {this.state.isRegisterOpen && <RegisterBox/>}
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
}
export default SignInUp;
