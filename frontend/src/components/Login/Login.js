import React from 'react'
import {Redirect, withRouter} from 'react-router-dom'
import { Form, Button, Container } from 'react-bootstrap'
import ApiInterface from '../../api/ApiInterface'
import config from '../../config'
import {checkLoggedIn} from "../../actions/actions";
import {connect} from "react-redux";
import styles from "../../App.scss";


class Login extends React.Component {

    constructor( props ) {
        super( props );
        this.loginInterface = new ApiInterface();
        
        this.state = {
            username : '', 
            password : '',
            error:''
        }

        this.choices = [
            ['kanye@west.com', 'y33zUs'],
            ['tame@impa.la', 'Kev!n'],
            ['travis@4getkylie.gov', 'Ht0wnH3ro']
        ] //TODO pick random for username/passowrd placeholders.

    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault();
        const { username, password} = this.state;
        console.log('will redirect after login to: ' + this.props.location.redirect || 'listen');
        const resp = await this.loginInterface.fetchLoginRedirect(
          'login/',
          { username, password, redirect: this.props.location.redirect || 'listen' });
        if (resp.url) {
          this.props.dispatch(checkLoggedIn())
        } else {
          this.setState({error: 'Invalid credentials.'})
        }
    };

    updateUsername = ( e ) => {
        const username = e.target.value;
        this.setState( { username, error: '' } )
    };

    updatePassword = ( e ) => {
        const password = e.target.value;
        this.setState( { password, error: '' } )
    };

    render() {
        if (this.props.user.isLoggedIn) {
            return (<Redirect to={this.props.location.redirect || (this.props.user.isController ? '/play' : '/listen')}/>)
        }
        return (
            <React.Fragment>
                <Container>
                    <h1 className={styles.body}>Login</h1>
                    <Form>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label className="font-weight-bold">username</Form.Label>
                            <Form.Control type="email" placeholder="username" onChange={this.updateUsername}/>
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label className="font-weight-bold" >password</Form.Label>
                            <Form.Control type="password" placeholder="password" onChange={this.updatePassword}
                                    isInvalid={this.state.error && '' !== this.state.error}/>
                            <Form.Control.Feedback type="invalid">
                                {this.state.error}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Button type="submit" onClick={this.loginInterfaceHandler }>
                            Login
                        </Button>
                        <Form.Text>need an account? <a href={"/signup"}>sign up</a></Form.Text>
                        <Form.Text><a href={config.API_BASE + '/accounts/password_reset'}>forgot your password?</a></Form.Text>
                    </Form>
                </Container>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(Login))