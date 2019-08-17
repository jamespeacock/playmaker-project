import React from 'react'
import Header from '../Header/Header'
import ApiInterface from '../../api/ApiInterface'
import './dashboard.css'
const uuid = require('uuid/v4')


export default class Login extends React.Component {

    static defaultProps = {
        history: {
          push: () => {}
        },
    }

    constructor ( props ) {
      super(props)
      this.state = {
            group : ''
        }
    }

    createGroup = async () => {
      return await new ApiInterface({}).get('controller/start')
    }

    findGroup = async () => {
      const path = 'listener/join?group=' + this.state.group
      return await new ApiInterface({}).get(path)
    }

    handlePlay = async () => {
        const { history } = this.props
        console.log('play')
        history.push({
          pathname: '/play',
          state: await this.createGroup()
        })
    }

    handleListen = async () => {
        const { history } = this.props
        history.push({
          pathname: '/listen',
          state: await this.findGroup()
        })
    }

    updateGroup = ( group ) => {
        this.setState( { group } )
    }

    render() {
        console.log('rendering dashboard')
        return (
            <React.Fragment>
                <Header></Header>
                <main className="dash-area">
                    <div className="button-container">
                        <div className="button-col-left">
                            <button
                                className="button"
                                onClick={this.handleListen}>
                                Listen
                            </button>
                        </div>
                        <div className="button-col-right">

                            <button
                                className="button"
                                onClick={this.handlePlay}>
                                Control Playback
                            </button>
                        </div>
                    </div>
                    <div className="group-container">
                        <label htmlFor="group_identifier" className="input-label">Group ID:</label>
                        <input  
                            type="text" 
                            name="username" 
                            className="form-input"
                            placeholder="spotify:user:rave_shepherd"
                            required
                            onChange={ keyInput => this.updateGroup( keyInput.target.value ) }>
                        </input>
                    </div>
                </main>
            </React.Fragment>
        )
    }
}