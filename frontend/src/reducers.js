import { combineReducers } from 'redux'
import {CHECK_LOGGED_IN} from './actions/actions.js'


//Define reducers here
function isLoggedIn(state = false, action) {
  switch (action.type) {
    case CHECK_LOGGED_IN:
      return action.isLoggedIn
      // const retLoggedIn = action.checkLoggedIn(setLoggedIn)
      // console.log("Returned from isLoggedIn:")
      // console.log(retLoggedIn)
      // return retLoggedIn
    default:
      return state
  }
  
}

const rootReducer = combineReducers({
  isLoggedIn
})

export default rootReducer