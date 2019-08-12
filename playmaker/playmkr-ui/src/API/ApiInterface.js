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
    console.log(process.env.REACT_APP_API_BASE)

    // bind options to interface and then deconstruct them.
    this.options = options
    const { method = 'GET', endpoint = 'login', body = false } = this.options
    // start building up the request endpoint.
    this.requestEndpoint = `${this.API_BASE}/${options.endpoint}`

    // start building up the request.

    // not all requests need a body. 
    if ( body ) {
      this.request_body = JSON.stringify( body )
    }
  }
  
  goFetch () {
    return fetch( this.requestEndpoint, this.request )
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

    fetchLoginRedirect () {
    return axios.post( this.requestEndpoint, this.request_body )
      .then( response => {
        return response
      })
      .then((res) => {
        console.log("res data url", res.data.url)
        return res.data.url
      })
  }
}
