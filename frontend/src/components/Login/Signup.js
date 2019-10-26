import React from 'react'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'
import {Button, Container, Form} from "react-bootstrap";
import {checkLoggedIn} from "../../actions/actions";

// const { Formik } = formik;

// const schema = yup.object({
//     firstName: yup.string().required(),
//     lastName: yup.string().required(),
//     username: yup.string().required(),
//     city: yup.string().required(),
//     state: yup.string().required(),
//     zip: yup.string().required(),
//     terms: yup.bool().required(),
// });

export default class Signup extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            name: '',
            username : '',
            email: '', 
            password1 : '',
            password2: '',
            error: ''
        }
    }

    signupHandler = async ( ) => {
        console.log('starting signupHandler')
        // evt.preventDefault()
        const { name, username, email, password1, password2 } = this.state;

        this.loginInterface = new ApiInterface();

        console.log('calling login redirect')
        const resp = await this.loginInterface.fetchLoginRedirect(
          'signup/',
          { name, email, username, password1, password2, redirect: 'dashboard'} //replace with this.props.redirect
        )
        if (resp.url) {
            this.props.dispatch(checkLoggedIn())
            window.location.href = resp.url
        } else {
            console.log('Failed to login. Please try again.')
            console.log(resp)
            this.setState({error: 'Invalid credentials.'})
        }
    }

    updateName = ( name ) => {
        this.setState( { name: name.target.value } )
    }

    updateEmail= ( email ) => {
        this.setState( { email: email.target.value } )
    }

    updateUsername = ( username ) => {
        this.setState( { username: username.target.value } )
    }

    updatePassword1 = ( password1 ) => {
        this.setState( { password1: password1.target.value } )
    }

    updatePassword2 = ( password2 ) => {
        this.setState( { password2: password2.target.value } )
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
                            <Form.Control type="username" placeholder="username" onChange={this.updateUsername}/>
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
                            <Form.Label>Confirm Password</Form.Label>
                            <Form.Control type="password" placeholder="password" onChange={this.updatePassword2}
                                          isInvalid={this.state.error && this.state.error != ''}/>
                            <Form.Control.Feedback type="invalid">
                                {this.state.error}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Button variant="primary" type="submit" onClick={this.signupHandler}>
                            Create Account
                        </Button>
                    </Form>
                </Container>
            </React.Fragment>
        )
    }
}