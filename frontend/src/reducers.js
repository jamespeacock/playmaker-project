import { combineReducers } from 'redux'
import {
    REFRESH_QUEUE_CONTROLLER,
    CHECK_LOGGED_IN,
    SET_CURRENT_DEVICE,
    REFRESH_DEVICES,
    START_CONTROLLER,
    UPDATE_CONTROLLER,
    START_LISTENER,
    CURRENT_SONG_SUCCESS,
    REFRESH_QUEUE_LISTENER,
    FETCH_ROOMS,
} from './actions/actions'

import {
    SHOW_DEVICES,
    SHOW_JOIN_ROOM,
    SHOW_REPORT
} from './actions/sessionActions'
import {LEAVE_ROOM} from "./actions/listenerActions";
import {CLOSE_ROOM} from "./actions/controllerActions";

const defaultUser = {
    isLoggedIn: false,
    isController: false,
    isListener: false,
    isInRoom: false,
    mode: '', // Can change this to broadcast, curate or listen...what else? broadcast/curate imply/require isController:true
    active_device: {},
    devices: []
}

//Define reducers here
function user(state=defaultUser, action) {
  switch (action.type) {
    case START_LISTENER:
        return Object.assign({}, state, {...state, isListener: true})
    case START_CONTROLLER:
        return Object.assign({}, state, {...state, isController: true})
    case CHECK_LOGGED_IN:
    case SET_CURRENT_DEVICE:
    case REFRESH_DEVICES:
    case LEAVE_ROOM:
    case CLOSE_ROOM:
        return Object.assign({}, state, action.user)
    default:
        return state
  }
}

function rooms(state=[], action) {
  switch (action.type) {
    case CHECK_LOGGED_IN:
    case FETCH_ROOMS:
      return Object.assign([], state, action.rooms)

    default:
      return state
  }
}

const defaultController = {
  queue: [],
  room: {},
  searchResults: {tracks: []},
  listeners: [],
  currentSong: {}
}

function controller(state=defaultController, action) {
  switch (action.type) {
  // case SEARCH
    case CURRENT_SONG_SUCCESS:
      return Object.assign({}, state, {...state, currentSong: action.current})
    case REFRESH_QUEUE_CONTROLLER:
      return Object.assign({}, state, action.actor)
    case CHECK_LOGGED_IN:
    case START_CONTROLLER:
    case UPDATE_CONTROLLER:
    case CLOSE_ROOM:
      return Object.assign({}, state, action.controller)
    default:
      return state
  }
}

const defaultListener = {
  queue: [],
  room: {},
  currentSong: {},
}

function listener(state=defaultListener, action) {
  switch (action.type) {
    case CURRENT_SONG_SUCCESS:
      return Object.assign({}, state, {...state, currentSong: action.current})
    case REFRESH_QUEUE_LISTENER:
      return Object.assign({}, state, action.actor)
    case START_LISTENER:
    case LEAVE_ROOM:
      return Object.assign({}, state, action.listener)
    default:
      return state
  }
}

const defaultSession = {
    showDevices: false,
    showReport: false,
    showJoinRoom: false
}

function session(state=defaultSession, action) {
    switch (action.type) {
        case SHOW_DEVICES:
        case SHOW_REPORT:
        case SHOW_JOIN_ROOM:
            return Object.assign({}, state, action.session)
        case SET_CURRENT_DEVICE:
            return Object.assign({}, state, {showDevices: false})
        case START_LISTENER:
            return Object.assign({}, state, {showJoinRoom: false})
        default:
            return state
    }
}

const playmakerApp = combineReducers({
    user,
    controller,
    listener,
    rooms,
    session
})

export default playmakerApp
