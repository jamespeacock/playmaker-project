import React from 'react'
import { Route, Switch, BrowserRouter } from 'react-router-dom'
import Controller from './components/Controller/Controller'
import Login from './components/Login/Login'
import Signup from './components/Login/Signup'
import Dashboard from './components/Login/Dashboard'
import Listener from './components/Listener/Listener'
import './App.css'
require('dotenv').config()

export default class App extends React.Component {

  render() {
    return (
    <BrowserRouter>
      <Switch>
        <Route
            path='/dashboard'
            component={ Dashboard }>
        </Route>
        <Route
            path='/play'
            component={ Controller }>
        </Route>
        <Route
            path='/listen'
            component={ Listener }>
        </Route>
        <Route
            path='/login'
            component={ Login }>
        </Route>
        <Route
            path='/signup'
            component={ Signup }>
        </Route>
      </Switch>
    </BrowserRouter>
    )
  }
}
