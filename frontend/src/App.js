import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Route, Switch, BrowserRouter } from 'react-router-dom'
import Controller from './components/Controller/Controller'
import Login from './components/Login/Login'
import Signup from './components/Login/Signup'
import Dashboard from './components/Login/Dashboard'
import Listener from './components/Listener/Listener'
import checkLoggedIn from './actions/actions'
import {CHECK_LOGGED_IN} from './actions/actions.js'
import './App.css'
require('dotenv').config()

class App extends React.Component {

  constructor(props) {
    super(props)
  }

  // checkLoggedIn = async () => {
  //     const isLoggedIn = await this.loginInterface.isLoggedIn()
  //     this.setState({isLoggedIn})
  // }

  componentWillMount () {
    // this.setState(store.getState());
    // store.subscribe(() => this.setState(store.getState()));
    console.log(this.props)
    const { dispatch } = this.props
    dispatch(checkLoggedIn())
  }

  render() {
    console.log('rendering app')
    console.log(this.props)
    return (
    <BrowserRouter>
      <Switch>
        <Route
            path='/dashboard'
            render={() => <Dashboard isLoggedIn={this.props.isLoggedIn} />}>
        </Route>
        <Route
            path='/play'
            render={() => <Controller isLoggedIn={this.props.isLoggedIn} />}>
        </Route>
        <Route
            path='/listen'
            render={() => <Listener isLoggedIn={this.props.isLoggedIn} />}>
        </Route>
        <Route
            path='/login'
            render={() => <Login isLoggedIn={this.props.isLoggedIn} />}>
        </Route>
        <Route
            path='/signup'
            render={() => <Signup isLoggedIn={this.props.isLoggedIn} />}>
        </Route>
      </Switch>
    </BrowserRouter>
    )
  }
}

App.propTypes = {
  isLoggedIn: PropTypes.bool.isRequired,
  dispatch: PropTypes.func.isRequired
}

function mapStateToProps(state) {
  // const { selectedSubreddit, postsBySubreddit } = state
  // const { isFetching, lastUpdated, items: posts } = postsBySubreddit[
  //   selectedSubreddit
  // ] || {
  //   isFetching: true,
  //   items: []
  // }
  const {isLoggedIn} = state;
  console.log('inAPP is logged in?')
  console.log(isLoggedIn)
  return {
    isLoggedIn
  }
}

export default connect(mapStateToProps)(App)
