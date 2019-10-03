import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import DeviceTable from '../shared/DeviceTable'
import SongTable from '../shared/SongTable'
import Header from '../Header/Header'
import './listener.css'
import {Redirect} from "react-router-dom";
import {Button} from "react-bootstrap";

export default class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            songs: [],
            devices: []
        }
        this.listener = new ListenerInterface()
    }

    componentDidMount() {
        this.refreshDevices()
        this.getAndLoadSongs()
    }

    refreshDevices = async ( ) => {
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
        if (!this.props.user.isLoggedIn) {
            return <Redirect to='/login' />
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
                        <Button onClick={this.refreshDevices}>Refresh Devices</Button>
                        <DeviceTable
                        devices={this.state.devices}
                        selectDeviceHandler={(deviceRow) => this.setDevice(deviceRow)} />
                    </section>
                </main>
            </React.Fragment>
        )
    }
}
