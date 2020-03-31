import ControllerInterface from "../api/ControllerInterface";


export const CLOSE_ROOM = "CLOSE_ROOM"

function closeRoom() {
    return async (dispatch, getState) => {
        let resp = await new ControllerInterface().close()
        let action = {type: CLOSE_ROOM}
        action.user = {
            isController: false,
            isInRoom: false
        }
        action.controller = {
            room: {},
            currentSong: {}
        }
        dispatch(action)
    }
}

export {
    closeRoom
}