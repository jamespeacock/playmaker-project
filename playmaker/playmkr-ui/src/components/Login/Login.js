import React from 'react'
import ApiInterface from '../../API/ApiInterface'

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
            method : 'GET', 
            endpoint : 'user', 
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
                  <form 
                    className="login_form"
                    onSubmit={submitEvent => this.loginInterfaceHandler( submitEvent )}>
                    <legend><h2 className="form_legend">Playmkr Login</h2></legend>
                    <div className="username_container">
                        <label htmlFor="username" className="input_label">Username:</label>
                        <input  
                            type="text" 
                            name="username" 
                            className="form_input"
                            placeholder="rave_shepherd"
                            onChange={ keyInput => this.updateUsername( keyInput.target.value ) }>
                        </input>
                    </div>
                    
                    <div className="password_container">
                        <label htmlFor="password" className="input_label">Password:</label>
                        <input 
                            type="text"
                            name="password" 
                            className="form_input"
                            placeholder="*****"
                            onChange={ keyInput => this.updatePassword( keyInput.target.value ) }>
                        </input>
                    </div>

                    <div className="form_submit_container">
                        <input 
                            type="submit" 
                            value="Login" 
                            className="submit_button">
                            
                        </input>
                    </div>
                </form>
            </React.Fragment>
        )
    }
}