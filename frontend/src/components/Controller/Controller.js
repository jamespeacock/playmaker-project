import React from 'react'
import Header from '../Header/Header'
import './controller.css'
import ApiInterface from '../../api/ApiInterface'
import ControllerInterface from '../../api/ControllerInterface'
import SongsInterface from '../../api/SongsInterface'
import SongTable from '../shared/SongTable'

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

        this.searchThrottled = debounce(1500, this.search);
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
        
        this.setState( { queue: songs } )
        this.setState( { isFetching: false } )
        //Then refresh recommendations

    }

    search = async (q ) => {
        const searchResults = await this.songsInterface.search(q)
        if (q == this.waitingFor) {
          this.setState( { searchResults } )
        }
    }

    changeQuery = event => {
      this.setState( { q:event.target.value },() => {
        if (this.state.q.length > 0) {
          this.waitingFor = this.state.q;
          this.searchThrottled(this.state.q)
        }
      } )
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
                            <input  
                                type="text" 
                                name="query" 
                                className="input-left"
                                placeholder="J. Cole"
                                required
                                onChange={this.changeQuery}>
                            </input>
                            <input 
                                type="submit" 
                                value="Search" 
                                className="submit-button"
                                onClick={e => this.search() }>
                            </input>
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