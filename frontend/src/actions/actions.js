import ApiInterface from '../api/ApiInterface'
import ControllerInterface from "../api/ControllerInterface";
import ListenerInterface from "../api/ListenerInterface";
import RoomInterface from '../api/RoomInterface'

export const CURRENT_SONG_SUCCESS = "CURRENT_SONG_SUCCESS";
export const CHECK_LOGGED_IN = 'CHECK_LOGGED_IN'
export const SET_CURRENT_DEVICE = 'SET_CURRENT_DEVICE'
export const REFRESH_DEVICES = 'REFRESH_DEVICES'
export const REFRESH_QUEUE_CONTROLLER = 'REFRESH_QUEUE_CONTROLLER'
export const REFRESH_QUEUE_LISTENER = 'REFRESH_QUEUE_LISTENER'
export const FETCH_ROOMS = 'FETCH_ROOMS'
export const START_CONTROLLER = 'START_CONTROLLER'
export const UPDATE_CONTROLLER = 'UPDATE_CONTROLLER'
export const START_LISTENER = 'START_LISTENER'

function checkLoggedIn(redirect = 'dashboard') {
  return async (dispatch, getState) => {
    const user = await new ApiInterface( {} ).isLoggedIn(redirect)
    let action = {
      type:CHECK_LOGGED_IN,
      user: {
        isLoggedIn: user.is_logged_in,
        isController: user.is_controller,
        isListener: user.is_listener,
        isInRoom: user.is_in_room,
        username: user.username,
        sp_username: user.sp_username,
        devices: user.devices,
        active_device: user.active_device,
        is_authenticated: user.is_authenticated,
        auth_url: user.auth_url
      }
    }
    if (user.is_listener) {
        action.listener = user.actor
        action.listener.room = action.listener.room || {}
    }
    if (user.is_controller) {
        action.controller = user.actor
    }
    dispatch(action)
  }
}

function fetchRooms( callback ) {
  return async (dispatch, getState) => {
    const rooms = await new RoomInterface().all()
    if (rooms) {
      const action = {
        type: FETCH_ROOMS,
        rooms
      }
      dispatch(action)
    }
    if (callback) {
      callback()
    }
  }
}

function setDevice( deviceRow ) {
  return async (dispatch, getState) => {
    const resp = await new ListenerInterface().setDevice(deviceRow.sp_id)
    if (resp) {
      const action = {
        type: SET_CURRENT_DEVICE,
        user: resp.user,
        listener: {room: {error: ''}},
        currentSong: resp.current_song
      }
      dispatch(action)
    }
  }
}

function updateMode( mode ) {
  return async (dispatch, getState) => {
    //TODO let this be used to switch btwn listenr & controller too
    await new ControllerInterface().updateMode(mode)
    // action = {type: SWITCH_MODE}
  }
}

function refreshDevices( ) {
  return async (dispatch, getState) => {
    const resp = await new ListenerInterface().devices()
    if (resp) {
      const action = {
        type: REFRESH_DEVICES,
        user: {
          devices: resp.devices,
          active_device: resp.active_device
        }
      }
    dispatch(action)
    }
  }
}

function editQueue( songUri, signalDone, position=null, toRemove=false) {
  return async (dispatch, getState) => {
    let action = {type: REFRESH_QUEUE_CONTROLLER}
    let resp = {success: false}
    if (toRemove && null !== position) {
      resp  = await new ControllerInterface().remove(songUri, position)
    } else if (!toRemove) {
      resp = await new ControllerInterface().add(songUri)
    }
    if (resp && resp.success) {
      action.actor = {
        currentSong: resp.currentSong ? resp.currentSong : {},
        queue: resp.queue ? resp.queue : []
      }
      dispatch(action)
    } else {
      //TODO make toast
      console.log("Failed to edit queue")
      action.actor = {queueFetching: false};
      dispatch(action)
    }
    signalDone()

  }
}

function refreshQueue( user , signalDone) {
  return async (dispatch, getState) => {
    let action = {type: 'listener' === user ? REFRESH_QUEUE_LISTENER : REFRESH_QUEUE_CONTROLLER}
    const resp = await new ControllerInterface({}).queue();
    if (resp && !resp.error) {
      action.actor = {
        currentSong: resp.currentSong ? resp.currentSong : {},
        queue: resp.queue ? resp.queue : [],
        roomClosed: false
      }
    } else {
      //Room is probably closed or controller is not playing music anymore
      action.actor = {
        roomClosed: true
      }
    }
    dispatch(action)
    signalDone()
  }
}

function nextSong(signalDone) {
  return async (dispatch, getState) => {
    const resp = await new ControllerInterface().next()
    dispatch(refreshQueue('controller', signalDone))
  }
}

function playSong(uri) {
  return async (dispatch, getState) => {
    const resp = await new ControllerInterface().play(uri)
    dispatch(getCurrentSong())
  }
}

function startController( mode, callback ) {
  return async (dispatch, getState) => {
    const controller = await new ControllerInterface({}).start(mode);
    console.log('start controller: ', controller)
    const action = {
      type: START_CONTROLLER,
      user: {
        isController: true
      },
      controller: {
        room: controller.room,
        queue: [],
        currentSong: controller.currentSong
      }
    };
    dispatch(action)
    if (callback) {
      callback()
    }
  }
}

function startListener(room, callback) {
  return async (dispatch, getState) => {
    const foundRoom = await new RoomInterface().getRoom(room);
    let action = {type: START_LISTENER,
      listener : { room: {} }
    }
    if (!foundRoom.id) {
      action.listener.room.error = "Room " + room + " does not exist."
      action.listener.isInRoom = false
      action.listener = {roomClosed: true};
    } else {
      const resp = await new ListenerInterface({}).joinRoom(foundRoom.id)
      if (resp && resp.room) {
        action.listener = resp;
        action.listener.roomClosed = false;
        action.listener.isInRoom = true;
        if (resp.error) {
          action.listener.room.error = resp.error;
        }
      }
      dispatch(action)
    }
    if (callback) {
      callback()
    }
  }
}

function getCurrentSong () {
    return async (dispatch, getState) => {
      const current =  await new ListenerInterface({}).current()
      console.log(current)
      if (current) {
        dispatch({type: CURRENT_SONG_SUCCESS, current: current.currentSong})
      } else {
        dispatch({type: CURRENT_SONG_SUCCESS, current: null})
      }
    }
}

function setRoomName (id, name) {
  return async (dispatch, getState) => {
    const room = await new RoomInterface().setRoomName(id, name)
    if (room) {
      dispatch({type: UPDATE_CONTROLLER, controller: {room}})
    }
  }

}

function submitReport (report) {
  return async (dispatch, getState) => {
    const type = report.isFeature ? "Feature Request" : "Bug/Problem"
    const description = report.text
    const resp = await new ApiInterface().post('feedback',
        {type, description}
    )
  }
}

export {
    checkLoggedIn,
    setDevice,
    refreshDevices,
    startController,
    startListener,
    getCurrentSong,
    refreshQueue,
    editQueue,
    nextSong,
    playSong,
    updateMode,
    fetchRooms,
    setRoomName,
    submitReport
}