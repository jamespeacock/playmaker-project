import ListenerInterface from "../api/ListenerInterface";

export const LEAVE_ROOM = 'LEAVE_ROOM'

function leaveRoom() {
    return async (dispatch, getState) => {
        let resp = await new ListenerInterface().leave()
        let action = {
            type: LEAVE_ROOM
        }
        if (!resp.error) {
            action.listener = {
                room: {},
            };
            action.user = {
                isInRoom: false,
                isListener: false
            };
            dispatch(action)
        } else {
            console.log("Error trying to leave room.")
        }
    }
}

export {
    leaveRoom
}