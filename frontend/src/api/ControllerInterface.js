import ApiInterface from './ApiInterface'

export default class ControllerInterface  {

  constructor( options ) {
    // bind options to interface and then deconstruct them.
    this.options = options
    this.apiInterface = new ApiInterface({})

  }

  updateMode = async ( mode ) => {
    return await this.apiInterface.put('controller/mode',
        {'mode': mode}
      )
  }

  start = async ( mode ) => {
    return await this.apiInterface.get('controller/start?mode=' + mode)
  }

 /* Get Current Room Queue */
  queue = async ( ) => {
    return await this.apiInterface.get('controller/queue')
  }

  add = async ( uri ) => {
    return await this.apiInterface.post('controller/queue/add',
     {'uris': [uri]}
     )
  }

  remove = async ( uri, pos ) => {
    return await this.apiInterface.post('controller/queue/remove',
     {'uris': [uri], 'positions': [pos]}
     )
  }

  /* Actions Section TODO these should all be PUT*/
  next = async ( ) => {
    return await this.apiInterface.get('controller/next')
  }

  play = async ( uri ) => {
    return await this.apiInterface.get(
      'controller/play?uris=' + uri
      )
  }

  seek = async ( position ) => {
    return await this.apiInterface.get(
      'controller/seek?position='+position
    )
  }

  close = async () => {
    return await this.apiInterface.get(
        'controller/close'
    )
  }

  /* Recommendations Section */
  recs = async ( ) => {
    return await this.apiInterface.get('controller/recs')
  }



}
