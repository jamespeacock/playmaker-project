import ApiInterface from '../api/ApiInterface'
import ListenerInterface from "../api/ListenerInterface";
export const CHECK_LOGGED_IN = 'CHECK_LOGGED_IN'
export const SET_CURRENT_DEVICE = 'SET_CURRENT_DEVICE'
export const REFRESH_DEVICES = 'REFRESH_DEVICES'

export const START_CONTROLLER = 'START_CONTROLLER'
export const START_LISTENER = 'START_LISTENER'

function checkLoggedIn() {
  return async (dispatch, getState) => {
    console.log('check logged in action called.')
    const user = await new ApiInterface( {} ).isLoggedIn()
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
        current_device: active_device
      },
      listener: {
        group: group
      }
    }
    console.log('actor', user.actor)
    dispatch(action)

  }
}

function setDevice( deviceRow ) {
  return async (dispatch, getState) => {
    console.log('set device action called.')
    const resp = await new ListenerInterface().setDevice(deviceRow.uri)
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

function refreshDevices( ) {
  console.log('refreshDevices called')
  return async (dispatch, getState) => {
    console.log('refresh devices action called.')
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

function startController( ) {
  console.log('start controller called');
  return async (dispatch, getState) => {
    console.log('start controller action called');
    const controller = await new ApiInterface({}).get('controller/start');
    // const controller = await new ControllerInterface().start() //TODO replace w/ this
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

function startListener(group, songs) {
  console.log('start listener called');
  return async (dispatch, getState) => {
    console.log('start listener action called')
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
      listener: {
        group: group,
        queue: songs
      }
    }
    dispatch(actionListener)
    dispatch(actionUser)
  }
}

export {
    checkLoggedIn,
    setDevice,
    refreshDevices,
    startController,
    startListener
}