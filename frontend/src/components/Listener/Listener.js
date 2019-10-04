import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import DevicesModal from '../shared/Devices'
import SongTable from '../shared/SongTable'
import Header from '../Header/Header'
import './listener.css'
import {Redirect} from "react-router-dom";


function ShowDevicesModal(props) {
    const [modalShow, setModalShow] = React.useState(true);
    console.log('in modal')
    console.log(props.user)
    if (false) {
        {/*<p>Listening on {this.props.user.selectedDevice.name}</p>*/}
        return (<p>Listening on Selected Device</p>)
    } else {
        return(<DevicesModal
            user={props.user}
            devices={props.devices}
            selectDeviceHandler={props.handler}
            show={modalShow}
            onHide={() => setModalShow(false)}
            />)
    }
};

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
        //set user selectedDevice name here with reducer
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
                        <ShowDevicesModal
                            user={this.props.user}
                            devices={this.state.devices}
                            handler={(deviceRow) => this.setDevice(deviceRow)}/>
                    </section>
                </main>

            </React.Fragment>
        )
    }
}
