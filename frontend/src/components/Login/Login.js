import React from 'react'
import { Redirect } from 'react-router-dom'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'
import './login.css'
import axios from 'axios';


export default class Login extends React.Component {

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
        const { username, password } = this.state
        const resp = await this.loginInterface.fetchLoginRedirect(
          'login/',
          { username, password, redirect: 'dashboard' })
        if (resp.url) {
          window.location.href = resp.url
        } else {
          console.log('Failed to get auth redirect. Please try again.')
        }
    }

    updateUsername = ( keyInput ) => {
        const username = keyInput.target.value
        this.setState( { username } )
    }

    updatePassword = ( keyInput ) => {
        const password = keyInput.target.value
        this.setState( { password } )
    }

    render() {
        console.log('rendering login')
        console.log(this.props.user.isLoggedIn)
        console.log(this.props.user)
        if (this.props.user.isLoggedIn) {
          //TODO jump to whatever is in "next" from initial request e.g. a room/dashboard/etc.
          return <Redirect to='/dashboard' />
        }
        // <Form>
        //   <Form.Group controlId="formBasicEmail">
        //     <Form.Label>Email address</Form.Label>
        //     <Form.Control type="email" placeholder="Enter email" />
        //     <Form.Text className="text-muted">
        //       We'll never share your email with anyone else.
        //     </Form.Text>
        //   </Form.Group>

        //   <Form.Group controlId="formBasicPassword">
        //     <Form.Label>Password</Form.Label>
        //     <Form.Control type="password" placeholder="Password" />
        //   </Form.Group>
        //   <Form.Group controlId="formBasicCheckbox">
        //     <Form.Check type="checkbox" label="Check me out" />
        //   </Form.Group>
        //   <Button variant="primary" type="submit">
        //     Submit
        //   </Button>
        // </Form>
        return (
            <React.Fragment>
                <Header user={this.props.user}></Header>
                <main className="login-area">
                    <form
                        className="login-form"
                        onSubmit={ submitEvent => this.loginInterfaceHandler( submitEvent ) }>
                        <legend><h2 className="form-legend">Login</h2></legend>
                        <div className="username-container">
                            <label htmlFor="username" className="input-label">Username:</label>
                            <input  
                                type="text" 
                                name="username" 
                                className="form-input"
                                placeholder="rave_shepherd"
                                required
                                onChange={this.updateUsername}>
                            </input>
                        </div>
                        <div className="password-container">
                            <label htmlFor="password" className="input-label">Password:</label>
                            <input 
                                type="password"
                                name="password" 
                                className="form-input"
                                required
                                placeholder="*******"
                                onChange={this.updatePassword}>
                            </input>
                        </div>

                        <div className="form-submit-container">
                            <input 
                                type="submit" 
                                value="Login" 
                                className="submit-button">
                            </input>
                        </div>
                    </form>
                </main>
            </React.Fragment>
        )
    }
}