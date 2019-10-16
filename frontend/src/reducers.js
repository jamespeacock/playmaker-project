import { combineReducers } from 'redux'
import {CHECK_LOGGED_IN, SET_CURRENT_DEVICE, REFRESH_DEVICES, START_CONTROLLER} from './actions/actions'

const defaultUser = {
    isLoggedIn: false,
    isController: false
}

//Define reducers here
function user(state = defaultUser, action) {
  console.log('in user reducer: ' + action.type)
  console.log('state', state)
  console.log(action.user)
  switch (action.type) {
    case CHECK_LOGGED_IN:
      return Object.assign({}, state, action.user)
    case SET_CURRENT_DEVICE:
      return Object.assign({}, state, action.user)
    case REFRESH_DEVICES:
      return Object.assign({}, state, action.user)
    default:
      return defaultUser
  }
}

const defaultController = {
  queue: [],
  group: [],
  searchResult: [],
  listeners: []
}

function controller(state=defaultController, action) {
  console.log('in controller reducer: ' + action.type)
  console.log('state', state)
  console.log(action.controller)
  switch (action.type) {
    case START_CONTROLLER:
      return Object.assign({}, state, action.controller)
    default:
      return Object.assign({}, state, action.controller)
  }
}

// Combine reducers to create root reducer below here.

function createReducer(initialState, handlers) {
  return function reducer(state = initialState, action) {
    if (handlers.hasOwnProperty(action.type)) {
      return handlers[action.type](state, action)
    } else {
      return state
    }
  }
}

const userReducer = createReducer({}, {
  user,
  controller
})

const playmakerApp = combineReducers({
  user: userReducer
})

export default playmakerApp
