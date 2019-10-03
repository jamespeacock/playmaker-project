import { combineReducers } from 'redux'
import {CHECK_LOGGED_IN} from './actions/actions.js'

const defaultUser = {
    isLoggedIn: false
}

//Define reducers here
function user(state = defaultUser, action) {
  switch (action.type) {
    case CHECK_LOGGED_IN:
      return Object.assign({}, state, action.user)
    default:
      return defaultUser
  }
}


const playmakerApp = combineReducers({
  user
})

export default playmakerApp
