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
import checkLoggedIn from './actions/actions'
import './App.css'
import ApiInterface from "./api/ApiInterface";
require('dotenv').config()

//This logic needs to live somewhere shared - how to get this to affect other components state??

class App extends React.Component {

  constructor(props) {
    super(props)
  }

  componentWillMount () {
    // this.setState(store.getState());
    // store.subscribe(() => this.setState(store.getState()));
    console.log(this.props)
    const { dispatch } = this.props
    dispatch(checkLoggedIn())
  }

  logout = async () => {
    console.log('logout clicked')
    await new ApiInterface().logout()
    this.props.dispatch(checkLoggedIn())
  }

  render() {
    console.log('rendering app with props')
    console.log(this.props)
    return (
    <AppContext.Provider value={{value:this.logout}}>
      <BrowserRouter>
        <Switch>
          <Route
              path='/dashboard'
              render={() => <Dashboard user={this.props.user} />}>
          </Route>
          <Route
              path='/play'
              render={() => <Controller user={this.props.user} />}>
          </Route>
          <Route
              path='/listen'
              render={() => <Listener user={this.props.user} />}>
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
  dispatch: PropTypes.func.isRequired
}

function mapStateToProps(state) {
  const { user } = state
  // const { isFetching, lastUpdated, items: posts } = postsBySubreddit[
  //   selectedSubreddit
  // ] || {
  //   isFetching: true,
  //   items: []
  // }
  console.log('mapping state to props')
  console.log(state)
  return {
    user
  }
}

export default connect(mapStateToProps)(App)
