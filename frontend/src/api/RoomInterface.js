import ApiInterface from './ApiInterface'

export default class RoomInterface {

    constructor(options) {
        // bind options to interface and then deconstruct them.
        this.options = options
        this.apiInterface = new ApiInterface({})

    }

    setRoomName = async (id, name) => {
        let room = {id, name}
        return await this.apiInterface.put('rooms/' + id,
            room
        )
    }

    all = async () => {
        return await this.apiInterface.get('rooms/all')
    }

}