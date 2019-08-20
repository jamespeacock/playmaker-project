import React from 'react'
import ApiInterface from '../../api/ApiInterface'
import Header from '../Header/Header'
import './login.css'
import axios from 'axios';


export default class Signup extends React.Component {

    static defaultProps = {
        history: {
          push: () => {}
        },
    }   

    constructor( props ) {
        super( props )
        this.state = {
            name: '',
            username : '',
            email: '', 
            password1 : '',
            password2: ''
        }
    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault()
        const { name, username, email, password1, password2 } = this.state
        const { history } = this.props

        this.loginInterface = new ApiInterface( {
            endpoint : 'signup/',
            body : { name, email, username, password1, password2 },
        } )

        //Redirect user to authentication url
        window.location.href = await this.loginInterface.fetchLoginRedirect()
        //Wait for above redirect to finish, then go to listener...but how
//        history.push('/listener')

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
                <Header></Header>
                <main className="login-area">
                    <form
                        className="login-form"
                        onSubmit={ submitEvent => this.loginInterfaceHandler( submitEvent ) }>
                        <legend><h2 className="form-legend">Login</h2></legend>
                        <div className="username-container">
                            <label htmlFor="name" className="input-label">Name:</label>
                            <input  
                                type="text" 
                                name="name" 
                                className="form-input"
                                placeholder="Rave"
                                required
                                onChange={ keyInput => this.updateName( keyInput.target.value ) }>
                            </input>
                            <label htmlFor="username" className="input-label">Username:</label>
                            <input  
                                type="text" 
                                name="username" 
                                className="form-input"
                                placeholder="rave_shepherd"
                                required
                                onChange={ keyInput => this.updateUsername( keyInput.target.value ) }>
                            </input>
                            <label htmlFor="email" className="input-label">Email:</label>
                            <input  
                                type="text" 
                                name="email" 
                                className="form-input"
                                placeholder="rave@shepherd.com"
                                required
                                onChange={ keyInput => this.updateEmail( keyInput.target.value ) }>
                            </input>
                        </div>
                        <div className="password-container">
                            <label htmlFor="password" className="input-label">Password:</label>
                            <input 
                                type="password"
                                name="password1" 
                                className="form-input"
                                required
                                placeholder="*******"
                                onChange={ keyInput => this.updatePassword1( keyInput.target.value ) }>
                            </input>
                        </div>
                        <div className="password-container">
                            <label htmlFor="password" className="input-label">Enter Password again:</label>
                            <input 
                                type="password"
                                name="password2" 
                                className="form-input"
                                required
                                placeholder="*******"
                                onChange={ keyInput => this.updatePassword2( keyInput.target.value ) }>
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