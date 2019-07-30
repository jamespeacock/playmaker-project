import React from 'react'
import ApiInterface from '../../API/ApiInterface'
import Header from '../Header/Header'
import './login.css'
import jQuery from 'jquery'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default class Login extends React.Component {

    static defaultProps = {
        history: {
          push: () => {}
        },
    }   

    constructor( props ) {
        super( props )
        this.state = {
            username : '', 
            password : ''
        }
    }

    loginInterfaceHandler = async ( evt ) => {
        evt.preventDefault()
        const { username, password } = this.state
        const { history } = this.props
        console.log(`Handling Login with creds —— username: ${username} and password: ${password}`)
        this.loginInterface = new ApiInterface( {
            method : 'POST', 
            endpoint : 'login/',
            body : { username, password },
        } )

        // Work this out depending on what's sent back...
//        const userLoggedIn = await this.loginInterface.goFetch()

        history.push('/listener')
    }

    updateUsername = ( username ) => {
        this.setState( { username } )
    }

    updatePassword = ( password ) => {
        this.setState( { password } )
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