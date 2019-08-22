import React from 'react'
import Header from '../Header/Header'
import './controller.css'
import ApiInterface from '../../api/ApiInterface'
import ControllerInterface from '../../api/ControllerInterface'
import SongTable from '../shared/SongTable'
import SearchBar from '../shared/Search'

import { debounce } from "throttle-debounce";

const uuid = require('uuid/v4')

export default class Controller extends React.Component {

    constructor( props ) {
        super( props )
        //TODO handle what happens if this page is loaded w/o controller + group
        this.state = {
            searchResults: [],
            recommendationResults: [],
            queue: [],
            isFetching: true,
            controller: this.props.location.state.controller,
            group: this.props.location.state.group,
            query: ''
        }
        this.searchHandler = this.searchHandler.bind(this)
    }

    componentDidMount() {
        this.initInterfaces()
        this.refreshQueueAndRecs()
    }

    initInterfaces = async ( ) => {
        this.controller = new ControllerInterface( {
            controller : this.state.controller
        } )
    }

    refreshQueueAndRecs = async ( ) => {
        //Refresh queue first
        this.setState( { isFetching: true } )
        const songs = await this.controller.queue()
        
        this.setState( { queue: songs } )
        this.setState( { isFetching: false } )
        //Then refresh recommendations

    }

    searchHandler(searchResults) {
        this.setState({searchResults})
    }

    render() {
        return (
            <React.Fragment>
                <Header></Header>
                <main className="main-area">
                    <div className="col-container">
                        <section className="controller-queue-container">
                            <div className="col-title">Queue</div>
                            <SongTable 
                            songs={this.state.queue} 
                            isFetching={this.state.isFetching}
                            withButtons={false}/>
                        </section>

                        <section className="search-container">
                          <div className="col-title">Search</div>
                            <SongTable 
                              songs={this.state.searchResults}
                              isFetching={this.state.isFetching}
                              withButtons={false}/>
                            <SearchBar setSearchResults={this.searchHandler} />
                        </section>

                    </div>
                    <div className="button-container">
                            <div className="button-col">
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