import React from 'react'
import { Provider } from 'react-redux'
import { Router, Route, BrowserRouter } from 'react-router-dom'
import App from './App'
import configureStore from './configureStore'
/*Replace with Redux React Router code as starting point to using REDUX*/

const store = configureStore()

export default class Root extends React.Component {
  render() {
    return (
      <Provider store={store}>
          <Root/>
      </Provider>
    )
  }
}
