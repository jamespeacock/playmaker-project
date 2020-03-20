import ApiInterface from '../api/ApiInterface'
import ListenerInterface from "../api/ListenerInterface";
import ControllerInterface from "../api/ControllerInterface";
// import {toastr} from "react-redux-toastr";

export const CURRENT_SONG_SUCCESS = "CURRENT_SONG_SUCCESS";
export const CHECK_LOGGED_IN = 'CHECK_LOGGED_IN'
export const SET_CURRENT_DEVICE = 'SET_CURRENT_DEVICE'
export const REFRESH_DEVICES = 'REFRESH_DEVICES'
export const REFRESH_QUEUE_CONTROLLER = 'REFRESH_QUEUE_CONTROLLER'
export const REFRESH_QUEUE_LISTENER = 'REFRESH_QUEUE_LISTENER'
// export const SEARCH = 'SEARCH'

export const START_CONTROLLER = 'START_CONTROLLER'
export const START_LISTENER = 'START_LISTENER'

function checkLoggedIn(redirect = 'dashboard') {
  return async (dispatch, getState) => {
    const user = await new ApiInterface( {} ).isLoggedIn(redirect)
    let devices = []
    let active_device = {};
    let group = '';
    if (user.actor) {
      devices = user.actor.devices || [];
      active_device = user.actor.active_device;
      group = user.actor.group;
    }
    const action = {
      type:CHECK_LOGGED_IN,
      user: {
        isLoggedIn: user.is_logged_in,
        isController: user.is_controller,
        isListener: user.is_listener,
        username: user.username,
        sp_username: user.sp_username,
        devices: devices,
        current_device: active_device,
        is_authenticated: user.is_authenticated,
        auth_url: user.auth_url
      },
      listener: {
        group: group
      }
    }
    dispatch(action)
  }
}

function setDevice( deviceRow ) {
  return async (dispatch, getState) => {
    const resp = await new ListenerInterface().setDevice(deviceRow.sp_id)
    if (resp.current_device) {
      const action = {
        type: SET_CURRENT_DEVICE,
        user: {
          current_device: resp.current_device
        }
      }
      dispatch(action)
    }
  }
  //replace with dispatch action here that calls listener.setDevice & set user selectedDevice (on user) name here with reducer
}

function updateMode( mode ) {
  //Is it ok to have this action that does not need to flow to a reducer
  return async (dispatch, getState) => {
    await new ControllerInterface().updateMode(mode)
  }
}

function refreshDevices( ) {
  return async (dispatch, getState) => {
    const devices = await new ListenerInterface().devices()
    if (devices) {
      const action = {
        type: REFRESH_DEVICES,
        user: {
          devices
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
    if (resp.success) {
      action.actor = {
        currentSong: resp.currentSong,
        queue: resp.queue
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
    action.actor = {
      currentSong: resp.currentSong,
      queue: resp.queue,
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

function startController( ) {
  return async (dispatch, getState) => {
    const controller = await new ControllerInterface({}).start();
    console.log('start controller: ', controller)
    const actionController = {
      type: START_CONTROLLER,
      controller: {
        group: controller.group,
        queue: []
      }
    };
    dispatch(actionController)
    const actionUser = {
      type: START_CONTROLLER,
      user: {
        isController: true
      }
    };
    dispatch(actionUser)
  }
}

function startListener(listener) {
  return async (dispatch, getState) => {
    const actionUser = {
      type: START_LISTENER,
      user: {
        isLoggedIn: true,
        isListener: true,
        isController: false
      }
    }
    const actionListener = {
      type: START_LISTENER,
      listener
    }
    dispatch(actionListener)
    dispatch(actionUser)
  }
}

// function search ( q ) {
//   return async (dispatch, getState) => {
    // let action = {type: SEARCH}
    // action.controller = { searchFetching: true}
    // dispatch(action)
    // //dispatch update search results
    // const searchResults = await this.songsInterface.search(q)
    // action.controller = {
    //   searchResults,
    //   searchFetching: false
    // }
    // dispatch(action)
//   }
// }

function getCurrentSong () {
    console.log('been called')
    return async (dispatch, getState) => {
      const current =  await new ListenerInterface({}).current()
      dispatch({type: CURRENT_SONG_SUCCESS, current})
    };
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
    updateMode
}