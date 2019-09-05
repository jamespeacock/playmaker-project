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
    console.log(this.API_BASE)

    // bind options to interface and then deconstruct them.
    this.options = options
    // start building up the request endpoint.

    this.axios = axios.create({
      baseURL: `${this.API_BASE}`,
      timeout: 2500,
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
  }
  
  get ( url ) {
    return this.axios.get( url )
      .then( response => {
        // throw an error when the response is empty
        if ( !response ) {
          throw "No response"
        }
        return response
      })
      .then((res) => res.data)
  }

  fetchLoginRedirect (url, body) {
    return this.axios.post( url, body )
      .then((res) => {
        return {url:res.data.url, error:res.data.error}
      })
  }

  isLoggedIn = async (url, body) => {
    return await this.axios.get( 'has_user' )
      .then((res) => {
        if ( !res ) {
          return false
        }
        return res.data.isLoggedIn
      })
  }

  logout = async () => {
    await this.axios.post('rest-auth/logout/')
  }
}
