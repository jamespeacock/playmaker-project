import React from 'react'
import Header from '../Header/Header'
import './controler.css'
import ApiInterface from '../../api/ApiInterface'
import ControllerInterface from '../../api/ControllerInterface'
import SongsInterface from '../../api/SongsInterface'
import SongTable from '../shared/SongTable'

const uuid = require('uuid/v4')

export default class Controller extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            searchResults: [],
            recommendationResults: [],
            queue: [],
            isFetching: true,
            controller: this.props.location.state.controller,
            group: this.props.location.state.group
        }
    }

    componentDidMount() {
        this.initInterfaces()
        this.refreshQueueAndRecs()
    }

    initInterfaces = async ( ) => {
        this.controller = new ControllerInterface( {
            controller : this.state.controller
        } )

        this.songsInterface = new SongsInterface( {

        })

    }

    refreshQueueAndRecs = async ( ) => {
        //Refresh queue first
        this.setState( { isFetching: true } )
        const songs = await this.controller.queue()
        console.log(songs)
        this.setState( { queue: songs } )
        this.setState( { isFetching: false } )
        //Then refresh recommendations

    }


    render() {
        console.log('rendering controller')
        return (
            <React.Fragment>
                <Header></Header>
                <main className="main-area">
                    <div className="col-container">
                        <section className="controller-queue-container">
                            <div className="col-title">Queue</div>
                            <SongTable songs={this.state.queue} isFetching={this.state.isFetching}/>
                        </section>

                        <section className="search-container">
                            <div className="col-title">Search</div>
                                <ul>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                </ul>
                        </section>

                        <section className="recommendations-container">
                            <div className="col-title">Listeners</div>
                                <ul>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                </ul>
                        </section>
                    </div>
                    <div className="button-container">
                            <div className="button-col-left">
                                <button
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handlePlay}>
                                    PLAY
                                </button>
                                <button
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handleSeek}>
                                    SEEK
                                </button>
                            </div>
                            <div className="button-col-right">
                                <button
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handleNext}>
                                    NEXT
                                </button>
                                <button
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handlePause}>
                                    PAUSE
                                </button>
                            </div>
                        </div>
                </main>
            </React.Fragment>
        )
    }
}