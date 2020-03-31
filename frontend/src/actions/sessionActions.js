

export const SHOW_DEVICES = 'SHOW_DEVICES'

function dispatchWrap(action) {
    return async (dispatch, getState) => {
        dispatch(action)
    }
}


function openDevices() {
    return async (dispatch, getState) => {
        let action = {
            type: SHOW_DEVICES,
            session: {
                showDevices: true
            }
        }
        dispatch(action)
    }
}

function hideDevices() {
    return async (dispatch, getState) => {
        let action = {
            type: SHOW_DEVICES,
            session: {
                showDevices: false
            }
        }
        dispatch(action)
    }
}

export const SHOW_REPORT = 'SHOW_REPORT'

function openReport() {
    console.log('open report called.')
    return async (dispatch, getState) => {
        let action = {
            type: SHOW_REPORT,
            session: {
                showReport: true
            }
        }
        dispatch(action)
    }
}

function hideReport() {
    return async (dispatch, getState) => {
        let action = {
            type: SHOW_REPORT,
            session: {
                showReport: false
            }
        }
        dispatch(action)
    }
}

export const SHOW_JOIN_ROOM = 'SHOW_JOIN_OROM'

function openJoinRoom() {
    return async (dispatch, getState) => {
        let action = {
            type: SHOW_JOIN_ROOM,
            session: {
                showJoinRoom: true
            }
        }
        dispatch(action)
    }
}

function hideJoinRoom() {
    return async (dispatch, getState) => {
        let action = {
            type: SHOW_JOIN_ROOM,
            session: {
                showJoinRoom: false
            }
        }
        dispatch(action)
    }
}

export {
    openDevices,
    hideDevices,
    openReport,
    hideReport,
    openJoinRoom,
    hideJoinRoom
}