import config from '../config'
import axios from 'axios';
import Cookies from 'js-cookie';
import ApiInterface from './ApiInterface'


export default class ListenerInterface  {

  constructor( options ) {
    this.apiInterface = new ApiInterface({})

  }

  queue = async ( ) => {
    return await this.apiInterface.get('listener/queue')
  }

  devices = async ( ) => {
    return await this.apiInterface.get('listener/devices')
  }

  setDevice = async ( deviceId ) => {
    return await this.apiInterface.post('listener/device', {'device': deviceId})
  }

}