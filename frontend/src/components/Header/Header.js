import React from 'react'
import './header.css'
import logo from '../../assets/logo.png'
import ApiInterface from '../../api/ApiInterface'
import { Redirect } from 'react-router-dom'
const uuid = require('uuid/v4')

export default class Header extends React.Component {

    static defaultProps = {
          history: {
            push: () => {}
          },
      }

    constructor (props) {
      super(props)
      this.logout = this.logout.bind(this)
    }

    //This logic needs to live somewhere shared - how to get this to affect other components state??
    logout = async () => {
        console.log('logout clicked')
        await new ApiInterface().logout()
        this.props.history.push({
            pathname: '/login',
            state: {isLoggedIn: false}
        })
    }

    render() {
        return (
            <header className="header-container">
                <img className="logo" alt="playmkr logo" src={logo}/>
                <button
                  key={uuid()}
                  onClick={this.logout}>
                  Log Out
              </button>
            </header>
        )
    }
}