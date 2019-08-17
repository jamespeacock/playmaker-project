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

  queue = async ( ) => {
    this.apiInterface.get('controller/queue?controller='+this.controller)
  }

  next = async ( ) => {
    this.nextApiInterface = new ApiInterface( {
        endpoint : 'controller/next?controller={0}'.format(this.controller)
    } )
    const next = await this.nextApiInterface.get()

  }

  pause = async ( ) => {
    this.pauseApiInterface = new ApiInterface( {
        endpoint : 'controller/pause?controller={0}'.format(this.controller)
    } )
    const pause = await this.pauseApiInterface.get()

  }

  play = async ( uri ) => {
    this.playApiInterface = new ApiInterface( {
        endpoint : 'controller/play?controller={0}&uris={1}'.format(this.controller, uri)
    } )
    const play = await this.playApiInterface.get()
  }

  seek = async ( position ) => {
    this.seekApiInterface = new ApiInterface( {
        endpoint : 'controller/seek?controller={0}&position={1}'.format(this.controller, position)
    } )
    const seek = await this.seekApiInterface.get()
  }


}
