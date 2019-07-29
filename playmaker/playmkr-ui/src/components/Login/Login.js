import React from 'react'
import ApiInterface from '../../API/ApiInterface'
import './login.css'

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
            endpoint : 'login', 
            body : { username, password }
        } )

        // Work this out depending on what's sent back... 
        const userLoggedIn = await this.loginInterface.goFetch()

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
                <header className="header-container">
                    <h2>play.mkr</h2>
                </header>
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