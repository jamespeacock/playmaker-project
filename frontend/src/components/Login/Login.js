import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { Form, Button, Container } from 'react-bootstrap'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'


class Login extends React.Component {

    static defaultProps = {
        history: {
          push: () => {}
        },
    }   

    constructor( props ) {
        super( props )
        this.loginInterface = new ApiInterface()
        
        this.state = {
            username : '', 
            password : ''
        }

    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault()
        const { username, password, redirect} = this.state
        const resp = await this.loginInterface.fetchLoginRedirect(
          'login/',
          { username, password, redirect })
        if (resp.url) {
          window.location.href = resp.url
        } else {
          console.log('Failed to get auth redirect. Please try again.')
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

    render() {
        if (this.props.user.isLoggedIn) {
          return <Redirect to={this.props.location.redirect || 'dashboard'} />
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
                            <Form.Control type="password" placeholder="Password" onChange={this.updatePassword}/>
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

export default withRouter(Login)