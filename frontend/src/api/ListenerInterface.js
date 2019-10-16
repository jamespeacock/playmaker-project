import ApiInterface from './ApiInterface'


export default class ListenerInterface  {

  constructor( options ) {
    this.apiInterface = new ApiInterface({})
  }

  queue = async ( ) => {
    return await this.apiInterface.get('listener/queue')
  }

  devices = async ( ) => {
    const devices = await this.apiInterface.get('listener/devices');
    return devices || [];
  }

  setDevice = async ( deviceId ) => {
    return await this.apiInterface.post('listener/devices', {'device': deviceId})
  }

}