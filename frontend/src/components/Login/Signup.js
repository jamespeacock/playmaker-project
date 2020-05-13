import React from 'react'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'
import {Button, Container, Form} from "react-bootstrap";
import {checkLoggedIn} from "../../actions/actions";
import {Redirect, withRouter} from 'react-router-dom'
import {connect} from "react-redux"

class Signup extends React.Component {

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

    signupHandler = async ( evt ) => {
        evt.preventDefault()
        const { name, username, email, password1, password2 } = this.state;
        // TODO validate all are non-empty

        this.loginInterface = new ApiInterface();

        const resp = await this.loginInterface.fetchLoginRedirect(
          'signup/',
          { name, email, username, password1, password2, redirect: this.props.location.redirect || 'dashboard'} //replace with this.props.redirect
        )
        if (resp.url) {
            console.log('resp had url')
            // this.props.dispatch(checkLoggedIn())
            window.location.href = resp.url
        } else {
            console.log('resp did not have url, error: ', resp.error)
            this.setState({error: resp.error})
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
        if (this.props.user.isLoggedIn) {
            return (<Redirect to={this.props.location.redirect || '/dashboard'}/>)
        }
        return (
            <React.Fragment>
                <Container>
                    <h2>Sign Up </h2>
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

                        <Button type="submit" onClick={this.signupHandler}>
                            Create Account
                        </Button>
                        <Form.Text onClick={() => this.props.history.push('/login')} >Have an account? Log In</Form.Text>
                    </Form>
                </Container>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(Signup))