import ApiInterface from '../api/ApiInterface'
export const CHECK_LOGGED_IN = 'CHECK_LOGGED_IN'

export default function checkLoggedIn(setLoggedIn) {
  return async (dispatch, getState) => {
    // dispatch(requestLoggedIn())
    const isLoggedIn = await new ApiInterface( {} ).isLoggedIn(setLoggedIn)
    console.log("In actions.js checkLoggedIn")
    console.log(isLoggedIn)
    dispatch({type:CHECK_LOGGED_IN, isLoggedIn: isLoggedIn})
    return isLoggedIn
   
  }
}
