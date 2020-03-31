import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Route, Switch, BrowserRouter } from 'react-router-dom'
import AppContext from './components/AppContext'
import Controller from './components/Controller/Controller'
import Login from './components/Login/Login'
import Signup from './components/Login/Signup'
import Dashboard from './components/Login/Dashboard'
import Room from './components/Listener/Room'
import Header from './components/Header/Header'
import {checkLoggedIn} from './actions/actions'
import './App.css'
import ApiInterface from "./api/ApiInterface";
import RoomList from "./components/rooms/RoomList";
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

  Dash = () => {
     return(<Dashboard
         user={this.props.user}
         controller={this.props.controller}
         listener={this.props.listener}
     />)
  }

  render() {
    return (
    <AppContext.Provider value={{logout:this.logout}}>
      <Header
          user={this.props.user}
          session={this.props.session}/>
      <BrowserRouter>
        <Switch>
          <Route exact path='/'
                 render={()=>this.Dash()}>
          </Route>
          <Route
              path='/dashboard'
              render={()=>this.Dash()}>
          </Route>
          <Route
              path='/play'
              render={() => <Controller
                  user={this.props.user}
                  controller={this.props.controller}
              />}>
          </Route>
          <Route
              exact path='/listen'
              render={() => <RoomList
                  user={this.props.user}
                  listener={this.props.listener}
                  rooms={this.props.rooms}
                  />}>
          </Route>
          <Route exact path="/listen/:id" render={() =><Room
              user={this.props.user}
              listener={this.props.listener}
              session={this.props.session}
              />}>
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
  rooms: PropTypes.array,
  session: PropTypes.object,
  dispatch: PropTypes.func.isRequired
}

function mapStateToProps(state) {
  //what the fuck should i be doing here???
  const { user, listener, controller, rooms, session } = state
  // const { isFetching, lastUpdated, items: posts } = postsBySubreddit[
  //   selectedSubreddit
  // ] || {
  //   isFetching: true,
  //   items: []
  // }
  return state
}

export default connect(mapStateToProps)(App)
