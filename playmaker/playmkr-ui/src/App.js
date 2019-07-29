import React from 'react'
import { Route, Switch } from 'react-router-dom'
import Controller from './components/Controller/Controller'
import Login from './components/Login/Login'
import Listener from './components/Listener/Listener'
import './App.css'
require('dotenv').config()

export default class App extends React.Component {

  render() {
    return (
      <Switch>
        <Route
            exact
            path='/controller'
            component={ Controller }>
        </Route>
        <Route
            exact
            path='/listener'
            component={ Listener }>
        </Route>
        <Route
            path='/'
            component={ Login }>
        </Route>
      </Switch>
    )
  }
}
