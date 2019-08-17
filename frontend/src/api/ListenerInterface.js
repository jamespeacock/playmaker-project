import config from '../config'
import axios from 'axios';
import Cookies from 'js-cookie';
import ApiInterface from './ApiInterface'


export default class ListenerInterface  {

  constructor( options ) {
    // bind options to interface and then deconstruct them.
    this.options = options
    const {listener = '-1'} = this.options
    this.listener = listener
    console.log('listener interface: ' + this.listener)
    this.apiInterface = new ApiInterface({})

  }

  queue = async ( ) => {
    return await this.apiInterface.get('listener/queue?listener='+this.listener)
  }

}