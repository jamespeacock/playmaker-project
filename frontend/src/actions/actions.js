import ApiInterface from '../api/ApiInterface'
export const CHECK_LOGGED_IN = 'CHECK_LOGGED_IN'

export default function checkLoggedIn() {
  return async (dispatch, getState) => {
    // dispatch(requestLoggedIn())
    const user = await new ApiInterface( {} ).isLoggedIn()
    console.log("In actions.js checkLoggedIn")
    console.log(user.isLoggedIn)
    console.log(user.username)
    const action = {type:CHECK_LOGGED_IN,
      user: {
        isLoggedIn: user.isLoggedIn,
        username: user.username,
        sp_username: user.sp_username
      }
    }
    dispatch(action)
   
  }
}
