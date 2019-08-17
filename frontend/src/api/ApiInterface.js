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
    const { endpoint = '', body = false } = this.options
    // start building up the request endpoint.

    this.axios = axios.create({
      baseURL: `${this.API_BASE}`,
      timeout: 2000,
      headers: {'Content-Type': 'application/json'}
    });

    // not all requests need a body. 
    if ( body ) {
      this.request_body = JSON.stringify( body )
    }
  }
  
  post (url) {
    return this.axios.post( url, this.request_body )
      .then( response => {
        // throw an error when the response is bad
        if ( !response.ok ) {
          return response
            .json()
            .then( error => {
              throw error
            })
        }
        // the next .then chainlinks see whether the response has any content. If the api sends an empty response
        // json() will throw an error because you passed it a null. So this handles the empty status 204 case.
        return response
      })
      .then((res) => res.text())
	    .then((text) => text.length ? JSON.parse(text) : {})
      .then( responseObj => responseObj )
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

  fetchLoginRedirect () {
    return this.axios.post( this.options.endpoint, this.request_body )
      .then((res) => {
        return res.data.url
      })
  }
}
