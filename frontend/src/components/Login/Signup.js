import React from 'react'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'
import {loginHandleErrors, validateInput} from "./shared";
import {Button, Container, Form} from "react-bootstrap";

const LoginHandleError = loginHandleErrors

export default class Signup extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            name: '',
            username : '',
            email: '', 
            password1 : '',
            password2: '',
            loginError: ''
        }
    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault()
        const { name, username, email, password1, password2 } = this.state;

        this.loginInterface = new ApiInterface();

        validateInput(this.setState);

        //This request will redirect to dashboard
        const resp = await this.loginInterface.fetchLoginRedirect(
          'signup/',
          { name, email, username, password1, password2, redirect: 'dashboard'} //replace with this.props.redirect
        )

        if (resp.url) {
          window.location.href = resp.url
        } else {
            this.setState((prevState, props) => {
                return { loginError: resp.error }
            })
        }

    }

    updateName = ( name ) => {
        this.setState( { name } )
    }

    updateEmail= ( email ) => {
        this.setState( { email } )
    }

    updateUsername = ( username ) => {
        this.setState( { username } )
    }

    updatePassword1 = ( password1 ) => {
        this.setState( { password1 } )
    }

    updatePassword2 = ( password2 ) => {
        this.setState( { password2 } )
    }

    render() {
        console.log('rendering login')
        return (
            <React.Fragment>
                <Header isLoggedIn={this.props.isLoggedIn} ></Header>
                <Container>
                    Sign Up
                    <Form>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label >Name</Form.Label>
                            <Form.Control type="username" placeholder="your name" onChange={this.updateName}/>
                        </Form.Group>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="email" placeholder="username" onChange={this.updateUsername}/>
                        </Form.Group>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Email</Form.Label>
                            <Form.Control type="email" placeholder="email" onChange={this.updateEmail}/>
                        </Form.Group>

                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="password" onChange={this.updatePassword1}/>
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Enter Password Again</Form.Label>
                            <Form.Control type="password" placeholder="password" onChange={this.updatePassword2}/>
                        </Form.Group>
                        <Button variant="primary" type="submit" onClick={this.loginInterfaceHandler}>
                            Create Account
                        </Button>
                        <LoginHandleError loginError={this.state.loginError}/>
                    </Form>
                </Container>
            </React.Fragment>
        )
    }
}