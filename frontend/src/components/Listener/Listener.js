import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import SongsInterface from '../../api/SongsInterface'
import QueueTable from '../shared/Queue'
import Header from '../Header/Header'
import './listener.css'
const uuid = require('uuid/v4')

export default class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            listener: this.props.location.state.listener,
            songs: [],
            isFetching: true
        }
    }
    componentDidMount() {
        this.initListener()
        this.getAndLoadSongs()
    }

    initListener = async ( ) => {
        this.listener = new ListenerInterface( {
          listener: this.state.listener
        } )
    }

    getAndLoadSongs = async ( ) => {
        this.setState( { isFetching: true } )
        const songs = await this.listener.queue()
        console.log(songs)
        this.setState( { songs: songs } )
        this.setState( { isFetching: false } )
    }

    render() {
        return (
            <React.Fragment>
                <Header></Header>
                <main className="listener-area">
                    <section className="listener-queue-container">
                        <h2 className="listener-queue-title">Listening Queue</h2>
                        <QueueTable songs={this.state.songs} isFetching={this.state.isFetching}/>
                    </section>
                </main>
            </React.Fragment>
        )
    }
}
