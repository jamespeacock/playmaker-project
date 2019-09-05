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
        
        this.loginInterface = new ApiInterface( {} )
        
        this.state = {
            username : '', 
            password : '',
            isLoggedIn: false,
        }

    }

    checkLoggedIn = async () => {
        const isLoggedIn = await this.loginInterface.isLoggedIn()
        this.setState({isLoggedIn})
    }

    componentWillMount () {
        this.checkLoggedIn()
    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault()
        const { username, password } = this.state
        const { history } = this.props
        const resp = await this.loginInterface.fetchLoginRedirect(
          'login/',
          { username, password, redirect: 'dashboard' })
        if (resp.url) {
          window.location.href = resp.url
        } else {
          console.log('Failed to get auth redirect. Please try again.')
        }
    }

    updateUsername = ( username ) => {
        this.setState( { username } )
    }

    updatePassword = ( password ) => {
        this.setState( { password } )
    }

    render() {
        console.log('rendering login')
        if (this.state.isLoggedIn) {
          console.log('jumping to dashboard.')
          //TODO jump to whatever is in "next" from initial request e.g. a room/dashboard/etc.
          this.props.history.push({
              pathname: '/dashboard',
              state: {isLoggedIn: true}
          })
        }
        return (
            <React.Fragment>
                <Header></Header>
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
                                onChange={ keyInput => this.updateUsername( keyInput.target.value ) }>
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
                                onChange={ keyInput => this.updatePassword( keyInput.target.value ) }>
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