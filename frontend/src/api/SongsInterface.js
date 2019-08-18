import config from '../config'
import axios from 'axios';
import Cookies from 'js-cookie';
import ApiInterface from './ApiInterface'

export default class SongsInterface  {

  constructor( options ) {
    // bind options to interface and then deconstruct them.
    this.options = options
    this.apiInterface = new ApiInterface({})
  }

  search = async ( q ) => {
    return await this.apiInterface.get('songs/search?q='+q)
  }

  

}