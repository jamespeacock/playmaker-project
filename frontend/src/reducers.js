import { combineReducers } from 'redux'
import {CHECK_LOGGED_IN, SET_CURRENT_DEVICE, REFRESH_DEVICES, START_CONTROLLER, START_LISTENER, CURRENT_SONG_SUCCESS} from './actions/actions'

const defaultUser = {
    isLoggedIn: false,
    isController: false,
    isListener: false
}

//Define reducers here
function user(state=defaultUser, action) {
//  console.log('in user reducer: ' + action.type)
//  console.log('state', state)
//  console.log(action.user)
  switch (action.type) {
    case CHECK_LOGGED_IN:
    case SET_CURRENT_DEVICE:
    case REFRESH_DEVICES:
    case START_LISTENER:
    case START_CONTROLLER:
      return Object.assign({}, state, action.user)
    default:
      return state
  }
}

const defaultController = {
  queue: [],
  group: '',
  searchResult: [],
  listeners: []
}

function controller(state=defaultController, action) {
//  console.log('in controller reducer: ' + action.type)
//  console.log('state', state)
//  console.log(action.controller)
  switch (action.type) {
    case START_CONTROLLER:
      return Object.assign({}, state, action.controller)
    default:
      return state
  }
}

const defaultListener = {
  queue: [],
  group: '',
  currentSong: {},
}

function listener(state=defaultListener, action) {
//  console.log('in listener reducer: ' + action.type)
//  console.log('state', state)
//  console.log(action.listener)
  switch (action.type) {
    case CURRENT_SONG_SUCCESS:
      console.log('CURR SONG STATE', state, action)
      return Object.assign({}, state, {...state, currentSong: action.current})
    case CHECK_LOGGED_IN:
    case START_LISTENER:
      console.log('START LISTENER', state)
      return Object.assign({}, state, action.listener)
    default:
      return state
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

// const userReducer = createReducer({}, {
//   user,
//   controller
// })

const playmakerApp = combineReducers({
  user,
  controller,
  listener
})

export default playmakerApp
