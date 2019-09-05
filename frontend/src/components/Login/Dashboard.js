import React from 'react'
import Header from '../Header/Header'
import ApiInterface from '../../api/ApiInterface'
import './dashboard.css'
const uuid = require('uuid/v4')


export default class Dashboard extends React.Component {

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
      var state = await new ApiInterface({}).get('controller/start')
      //replace this shit with redux. have isLoggedIn live in ONE place
      state.isLoggedIn = this.props.location.state.isLoggedIn
      return state
    }

    findGroup = async () => {
      const path = 'listener/join?group=' + this.state.group
      var state = await new ApiInterface({}).get(path)
      state.isLoggedIn = this.props.location.state.isLoggedIn
      return state
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
        if (!this.props.location.state || this.props.location.state.isLoggedIn != true) {
          this.props.history.push('/login')
        }
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