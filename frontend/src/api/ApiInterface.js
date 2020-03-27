import config from '../config'
import axios from 'axios';
import Cookies from 'js-cookie';


export default class ApiInterface  {
    
  constructor( options ) {
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.withCredentials = true;
    // import api configuration.
    this.API_BASE = config.API_BASE

    // bind options to interface and then deconstruct them.
    this.options = options
    // start building up the request endpoint.

    this.axios = axios.create({
      baseURL: `${this.API_BASE}`,
      timeout: 150000,
      headers: {'Content-Type': 'application/json'}
    });

  }
  
  post (url, body) {
    return this.axios.post( url, JSON.stringify(body) )
      .then( response => {
        // throw an error when the response is bad
        if ( !response ) {
          throw "No response!"
        }
        return response
      })
      .then((res) => res.data)
        .catch(e => {
            console.log("errored", e.response)
            if (e.response.status != 500) {
                return e.response.data
            }
        })
  }
  
  get ( url ) {
    //TODO Make these errors throw toasts so I can see their errors
    return this.axios.get( url )
      .then( response => {
        // throw an error when the response is empty
        if ( !response ) {
          throw "No response"
        }
        return response
      })
      .then((res) => res.data)
        .catch(e => {
            if (e.response.status != 500) {
                return e.response.data
            }
        })
  }

    put ( url, body) {
        //TODO Make these errors throw toasts so I can see their errors
        return this.axios.put( url, JSON.stringify(body) )
            .then( response => {
                // throw an error when the response is empty
                if ( !response ) {
                    throw "No response"
                }
                return response
            })
            .then((res) => res.data)
            .catch(e => {
                if (e.response.status != 500) {
                    return e.response.data
                }
            })
    }

  fetchLoginRedirect (url, body) {
    return this.axios.post( url, body)
      .then((res) => {
          if (!res) {
            return {error: 'No data. Server Error'}
          }
        return {url:res.data.url, error:res.data.error}
      })
        .catch((e) => e.response.data)
  }

  async isLoggedIn(redirect) {
    return await this.axios.get( 'has_user?redirect=' + redirect )
      .then((res) => {
        if (res.data.user) {
          return res.data.user
        } else {
          return {isLoggedIn: false}
        }
      })
      .catch((res) => {
        return {isLoggedIn: false}
      })
  }

  logout = async () => {
    await this.axios.post('login/logout').catch(e => {
        return {error: e.response.data}
    })
  }
}
