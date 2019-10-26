import React from 'react'
import {Redirect, withRouter} from 'react-router-dom'
import { Form, Button, Container } from 'react-bootstrap'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'
import {checkLoggedIn} from "../../actions/actions";
import {connect} from "react-redux";


class Login extends React.Component {

    constructor( props ) {
        super( props )
        this.loginInterface = new ApiInterface()
        
        this.state = {
            username : '', 
            password : '',
            error:''
        }

    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault()
        const { username, password} = this.state
        const resp = await this.loginInterface.fetchLoginRedirect(
          'login/',
          { username, password, redirect: this.props.location.redirect || 'dashboard' })
        if (resp.url) {
          this.props.dispatch(checkLoggedIn())
          window.location.href = resp.url
        } else {
          console.log('Failed to login. Please try again.')
          console.log(resp)
          this.setState({error: 'Invalid credentials.'})
        }
    }

    updateUsername = ( e ) => {
        const username = e.target.value;
        this.setState( { username } )
    }

    updatePassword = ( e ) => {
        const password = e.target.value;
        this.setState( { password } )
    }

    // componentWillMount() {
    //     this.props.dispatch(checkLoggedIn())
    // }

    render() {
        console.log('rendering', this.state.error)
        if (this.props.user.isLoggedIn) {
            return (<Redirect to={this.props.location.redirect || '/dashboard'}/>)
        }
        return (
            <React.Fragment>
                <Header user={this.props.user}></Header>
                <Container>
                    <Form>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="username" placeholder="email or username" onChange={this.updateUsername}/>
                            <Form.Text className="text-muted">
                                We'll never share your email with anyone else.
                            </Form.Text>
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password" onChange={this.updatePassword}
                                    isInvalid={this.state.error && this.state.error != ''}/>
                            <Form.Control.Feedback type="invalid">
                                {this.state.error}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Button variant="primary" type="submit" onClick={this.loginInterfaceHandler }>
                            Login
                        </Button>
                    </Form>
                </Container>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(Login))