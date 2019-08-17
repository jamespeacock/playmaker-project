import React from 'react'
import Header from '../Header/Header'
import './controler.css'

import ApiInterface from '../../api/ApiInterface'
import ControllerInterface from '../../api/ControllerInterface'
import SongsInterface from '../../api/SongsInterface'

const uuid = require('uuid/v4')

//Replace lists with working list display code from listener.js
export default class Controller extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            searchResults: [],
            recommendationResults: [],
            queue: [],
            controller: this.props.location.state.controller,
            group: this.props.location.state.group
        }
    }

    componentDidMount() {
        this.initController()
        this.refreshQueueAndRecs()
        
    }

    initController = async ( ) => {
        this.controller = new ControllerInterface( {
            controller : this.state.controller
        } )

    }

    refreshQueueAndRecs = async ( ) => {
        //Refresh queue first
        const songsList = await this.controller.queue()
        this.state.queue = songsList

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
                            <ul>

                            </ul>
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