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
        this.addToQueueHandler = this.addToQueueHandler.bind(this)
    }

    componentDidMount() {
        this.initInterfaces()
        this.refreshQueue()
    }

    initInterfaces = async ( ) => {
        this.controller = new ControllerInterface( {
            controller : this.state.controller
        } )
    }

    refreshQueue = async ( ) => {
        this.setState( { isFetching: true } )
        const songs = await this.controller.queue()
        this.setState( { queue: songs } )
        this.setState( { isFetching: false } )
        //Then refresh recommendations

    }

    searchHandler(searchResults) {
        this.setState({searchResults})
    }

    addToQueueHandler = async (songRow) => {
      console.log('adding ' + songRow.name + ' to queue.')
      const success = await this.controller.add(songRow.uri)
      console.log(success)
      if (success) {
        this.refreshQueue()
      } else { 
        console.log('Could not add song to queue')
      }
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
                            <SearchBar setSearchResults={this.searchHandler} />
                            <SongTable 
                              songs={this.state.searchResults}
                              isFetching={this.state.isFetching}
                              withButtons={true}
                              handleAdd={(row) => this.addToQueueHandler(row)}/>
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