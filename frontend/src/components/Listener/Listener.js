import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import SongsInterface from '../../api/SongsInterface'
import DeviceTable from '../shared/DeviceTable'
import SongTable from '../shared/SongTable'
import Header from '../Header/Header'
import './listener.css'
const uuid = require('uuid/v4')

export default class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            songs: [],
            devices: []
        }
    }

    componentDidMount() {
        this.initListener()
        this.getAndLoadSongs()
    }

    initListener = async ( ) => {
        this.listener = new ListenerInterface()
        this.state.devices = await this.listener.devices()
    }

    getAndLoadSongs = async ( ) => {
        const songs = await this.listener.queue()
        this.setState( { songs: songs } )
    }

    setDevice = async ( deviceRow ) => {
      const success = await this.listener.setDevice(deviceRow.uri)
    }

    render() {
        if (!this.props.location.state || !this.props.location.state.isLoggedIn) {
          this.props.history.push('/login')
        }
        return (
            <React.Fragment>
                <Header></Header>
                <main className="listener-area">
                    <section className="listener-queue-container">
                        <h2 className="listener-queue-title">Listening Queue</h2>
                        <SongTable
                        songs={this.state.songs}
                        withButtons={false}/>
                    </section>
                    <section className="listener-devices-container">
                        <h2 className="listener-devices-title">Your Devices</h2>
                        <DeviceTable
                        devices={this.state.devices}
                        selectDeviceHandler={(deviceRow) => this.setDevice(deviceRow)} />
                    </section>
                </main>
            </React.Fragment>
        )
    }
}
