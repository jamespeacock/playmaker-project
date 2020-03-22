import { combineReducers } from 'redux'
import {
  REFRESH_QUEUE_CONTROLLER,
  CHECK_LOGGED_IN,
  SET_CURRENT_DEVICE,
  // SEARCH,
  REFRESH_DEVICES,
  START_CONTROLLER,
  START_LISTENER,
  CURRENT_SONG_SUCCESS,
  REFRESH_QUEUE_LISTENER
} from './actions/actions'

const defaultUser = {
    isLoggedIn: false,
    isController: false,
    isListener: false,
    mode: '' // Can change this to broadcast, curate or listen...what else? broadcast/curate imply/require isController:true
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
  searchResults: {tracks: []},
  listeners: [],
  currentSong: {}
}

function controller(state=defaultController, action) {
//  console.log('in controller reducer: ' + action.type)
//  console.log('state', state)
//  console.log(action.controller)
  switch (action.type) {
  // case SEARCH
    case CURRENT_SONG_SUCCESS:
      return Object.assign({}, state, {...state, currentSong: action.current})
    case REFRESH_QUEUE_CONTROLLER:
      return Object.assign({}, state, action.actor)
    case CHECK_LOGGED_IN:
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
      return Object.assign({}, state, {...state, currentSong: action.current})
    case REFRESH_QUEUE_LISTENER:
      return Object.assign({}, state, action.actor)
    case CHECK_LOGGED_IN:
    case START_LISTENER:
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

const playmakerApp = combineReducers({
  user,
  controller,
  listener
})

export default playmakerApp
