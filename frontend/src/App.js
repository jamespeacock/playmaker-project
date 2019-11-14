import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Route, Switch, BrowserRouter } from 'react-router-dom'
import AppContext from './components/AppContext'
import Controller from './components/Controller/Controller'
import Login from './components/Login/Login'
import Signup from './components/Login/Signup'
import Dashboard from './components/Login/Dashboard'
import Listener from './components/Listener/Listener'
import Header from './components/Header/Header'
import {checkLoggedIn} from './actions/actions'
import './App.css'
import ApiInterface from "./api/ApiInterface";
require('dotenv').config()

class App extends React.Component {

  constructor(props) {
    super(props)
  }

  logout = async () => {
    await new ApiInterface().logout()
    this.props.dispatch(checkLoggedIn())
  }

  componentWillMount() {
    this.props.dispatch(checkLoggedIn())
  }

  render() {
    return (
    <AppContext.Provider value={{user:this.props.user, logout:this.logout}}>
      <Header/>
      <BrowserRouter>
        <Switch>
          <Route exact path='/'
                 render={() => <Dashboard user={this.props.user} />}>
          </Route>
          <Route
              path='/dashboard'
              render={() => <Dashboard user={this.props.user} />}>
          </Route>
          <Route
              path='/play'
              render={() => <Controller
                  user={this.props.user}
                  controller={this.props.controller}
              />}>
          </Route>
          <Route
              path='/listen'
              render={() => <Listener
                  user={this.props.user}
                  listener={this.props.listener}/>}>
          </Route>
          <Route
              path='/login'
              render={() => <Login user={this.props.user} />}>
          </Route>
          <Route
              path='/signup'
              render={() => <Signup user={this.props.user} />}>
          </Route>
        </Switch>
      </BrowserRouter>
    </AppContext.Provider>
    )
  }
}

App.propTypes = {
  user: PropTypes.object.isRequired,
  controller: PropTypes.object,
  listener: PropTypes.object,
  dispatch: PropTypes.func.isRequired
}

function mapStateToProps(state) {
  //what the fuck should i be doing here???
  const { user, listener, controller } = state
  // const { isFetching, lastUpdated, items: posts } = postsBySubreddit[
  //   selectedSubreddit
  // ] || {
  //   isFetching: true,
  //   items: []
  // }
  return state
}

export default connect(mapStateToProps)(App)
