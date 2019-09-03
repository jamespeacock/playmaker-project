import React from 'react'
import './header.css'
import logo from '../../assets/logo.png'
import ApiInterface from '../../api/ApiInterface'
import { Redirect } from 'react-router-dom'
const uuid = require('uuid/v4')

export default class Header extends React.Component {

  constructor (props) {
    super(props)
    
    this.state = {
      isLoggedIn:true
    }
    this.logout = this.logout.bind(this)
  }

  logout = async () => {
      await new ApiInterface().logout()
      this.setState({isLoggedIn:false})
  }

  render() {
    if (this.state.isLoggedIn) {
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
    } else {
      return (
        <Redirect to="/login"/>
      )
    }
  }
}