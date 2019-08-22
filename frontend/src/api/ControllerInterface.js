import config from '../config'
import axios from 'axios';
import Cookies from 'js-cookie';
import ApiInterface from './ApiInterface'


export default class ControllerInterface  {

  constructor( options ) {
    // bind options to interface and then deconstruct them.
    this.options = options
    const {controller = '-1'} = this.options
    this.controller = controller
    console.log('controller interface: ' + this.controller)
    this.apiInterface = new ApiInterface({})

  }

 /* Get Current Room Queue */
  queue = async ( ) => {
    return await this.apiInterface.get('controller/queue?controller='+this.controller)
  }

  add = async ( uri ) => {
    return await this.apiInterface.post('controller/queue/add/',
     {'controller':this.controller,'uris': [uri]}
     )
  }

  remove = async ( uri ) => {
    return await this.apiInterface.post('controller/queue/remove/',
     {'controller':this.controller,'uris': [uri]}
     )
  }

  /* Actions Section */
  next = async ( ) => {
    return await this.apiInterface.get('controller/next?controller='+this.controller)
  }

  pause = async ( ) => {
    return await this.apiInterface.get('controller/pause?controller='+this.controller)
  }

  play = async ( uri ) => {
    return await this.apiInterface.get(
      'controller/play?controller={0}&uris={1}'.format(this.controller, uri)
      )
  }

  seek = async ( position ) => {
    return await this.apiInterface.get(
      'controller/seek?controller={0}&position={1}'.format(this.controller, position)
    )
  }

  /* Recommendations Section */
  recs = async ( ) => {
    return await this.apiInterface.get('controller/recs')
  }


}
