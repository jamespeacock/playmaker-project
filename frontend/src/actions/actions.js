import ApiInterface from '../api/ApiInterface'
import ListenerInterface from "../api/ListenerInterface";
export const CHECK_LOGGED_IN = 'CHECK_LOGGED_IN'
export const SET_CURRENT_DEVICE = 'SET_CURRENT_DEVICE'
export const REFRESH_DEVICES = 'REFRESH_DEVICES'

export const START_CONTROLLER = 'START_CONTROLLER'

function checkLoggedIn() {
  return async (dispatch, getState) => {
    console.log('check logged in action called.')
    const user = await new ApiInterface( {} ).isLoggedIn()
    const action = {
      type:CHECK_LOGGED_IN,
      user: {
        isLoggedIn: user.isLoggedIn,
        isController: false,
        username: user.username,
        sp_username: user.sp_username,
        devices: user.devices || [],
        current_device: user.current_device
      }
    }
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
        group: 'default',
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
export {
    checkLoggedIn,
    setDevice,
    refreshDevices,
    startController
}