import React from 'react'
import Header from '../Header/Header'
import { Redirect, withRouter } from 'react-router-dom'
import './controller.css'
import ControllerInterface from '../../api/ControllerInterface'
import SongTable from '../shared/SongTable'
import SearchBar from '../shared/Search'
import {Card} from "react-bootstrap";


const uuid = require('uuid/v4')

class Controller extends React.Component {

    constructor( props ) {
        super( props )
        console.log(props)
        //TODO handle what happens if this page is loaded w/o controller + group
        this.state = {
            searchResults: {'tracks':[]},
            recommendationResults: [],
            queue: [],
            query: '',
            group: this.props.location.state.group,
        }
        this.searchHandler = this.searchHandler.bind(this)
        this.addToQueueHandler = this.addToQueueHandler.bind(this)
        this.handleNext = this.handleNext.bind(this)
        this.handlePause = this.handlePause.bind(this)
        this.handlePlay = this.handlePlay.bind(this)
        this.handleSeek = this.handleSeek.bind(this)
        
    }

    async handleNext() {
      await this.controller.next()
      this.refreshQueue()
    }

    handlePause() {
      this.controller.pause()
    }

    handlePlay( uri ) {
        this.controller.play(uri)
    }

    handleSeek( position ) {
        this.controller.seek(position)
    }


    componentDidMount() {
        this.initInterfaces()
        this.refreshQueue()
    }

    initInterfaces = async ( ) => {
        this.controller = new ControllerInterface()
    }

    refreshQueue = async ( ) => {
        const songs = await this.controller.queue()
        //dispatch update queue
        this.setState( { queue: songs } )
    }

    searchHandler(searchResults) {
        //dispatch update search results
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

    removeFromQueueHandler = async (songRow) => {
      console.log('removing ' + songRow.name + ' from queue.')
      const success = await this.controller.remove(songRow.uri, songRow.position)
      console.log(success)
      if (success) {
        this.refreshQueue()
      } else { 
        console.log('Could not remove song from queue')
      }
    }

    render() {
        if (!this.props.user.isLoggedIn) {
            return <Redirect to='/login' />
        }
        return (
            <React.Fragment>
                <Header></Header>
                <Card style={{ width: '18rem' }}>
                    <Card.Body>
                        <Card.Text style={{color: 'black'}}>
                            {this.state.group}
                        </Card.Text>
                    </Card.Body>
                </Card>
                <main className="main-area">
                    <div className="col-container">
                        <section className="controller-queue-container">
                            <div className="col-title">Queue</div>
                            <SongTable 
                            songs={this.state.queue}
                            withButtons={true}
                            handleAdd={this.removeFromQueueHandler}/>
                        </section>

                        <section className="search-container">
                          <div className="col-title">Search</div>
                            <SearchBar setSearchResults={this.searchHandler} />
                            <SongTable 
                              songs={this.state.searchResults.tracks}
                              withButtons={true}
                              handleAdd={this.addToQueueHandler}/>
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

export default withRouter(Controller);