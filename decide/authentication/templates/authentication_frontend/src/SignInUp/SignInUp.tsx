import React from 'react';
import { Alert, Button, ButtonGroup, Card, Col, Container, Row } from 'react-bootstrap';
import './index.css';
import LoginBox from './Login';
import RegisterBox from './Register';
import LoginLDAP from "./LoginLDAP";

class SignInUp extends React.Component<any, State>{

  constructor(props: any) {
    super(props);
    this.state = {
      isLoginOpen: true,
      isRegisterOpen: false,
      isLoginLDAPOpen: false,
    };
  }

  showLoginBox() {
    this.setState({ isLoginOpen: true, isRegisterOpen: false, isLoginLDAPOpen: false });
  }

  showRegisterBox() {
    this.setState({ isRegisterOpen: true, isLoginOpen: false, isLoginLDAPOpen: false });
  }

  showLoginLDAP() {
    this.setState({ isRegisterOpen: false, isLoginOpen: false, isLoginLDAPOpen: true });
  }

  render() {
    console.log(this.state)
    return (
      <Container>
        <Card className="mx-auto text-center rounded-3" >
          <Card.Body>
            <Card.Title>
              {this.state.isLoginOpen && <h4>LOGIN</h4>}
              {this.state.isRegisterOpen && <h4>REGISTER</h4>}
              {this.state.isLoginLDAPOpen && <h4>LOGIN LDAP</h4>}
            </Card.Title>
            <Card.Text>
              {this.state.isLoginOpen && <LoginBox />}
              {this.state.isRegisterOpen && <RegisterBox />}
              {this.state.isLoginLDAPOpen && <LoginLDAP />}
              <br />
              {this.state.isLoginOpen && <><p>Would you prefer to log in via LDAP? Click <a className="link" onClick={this
                .showLoginLDAP
                .bind(this)}>here</a></p><p>Not a member yet? Click <a className="link" onClick={this
                  .showRegisterBox
                  .bind(this)}>here</a> to join </p></>}
              {this.state.isRegisterOpen && <p>Do you already have an account? Sign in <a className="link" onClick={this
                .showLoginBox
                .bind(this)}>here</a> or via <a className="link" onClick={this
                  .showLoginLDAP
                  .bind(this)}>LDAP</a> </p>}
              {this.state.isLoginLDAPOpen && <p>Not a member yet? Click <a className="link" onClick={this
                .showRegisterBox
                .bind(this)}>here</a> to join</p>}
            </Card.Text>
          </Card.Body>
        </Card>
      </Container>
    );
  }

}

interface State {
  isRegisterOpen: boolean,
  isLoginOpen: boolean
  isLoginLDAPOpen: boolean
}
export default SignInUp;
