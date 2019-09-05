import React from 'react'
// import { Provider } from 'react-redux'
import { Route, Switch, BrowserRouter } from 'react-router-dom'
import Controller from './components/Controller/Controller'
import Login from './components/Login/Login'
import Signup from './components/Login/Signup'
import Dashboard from './components/Login/Dashboard'
import Listener from './components/Listener/Listener'
import './App.css'
require('dotenv').config()

/*Replace with Redux React Router code as starting point to using REDUX
const Root = ({ store }) => (
  <Provider store={store}>
    <Router>
      <Route path="/" component={App} />
    </Router>
  </Provider>
)
*/
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
