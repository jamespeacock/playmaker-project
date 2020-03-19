import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import ControllerInterface from '../../api/ControllerInterface'
import SongTable from '../shared/SongTable'
import SearchBar from '../shared/Search'
import {Card} from "react-bootstrap";
import {connect} from "react-redux";
import {checkLoggedIn, startController} from "../../actions/actions";
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";


const uuid = require('uuid/v4')

class Controller extends React.Component {

    constructor( props ) {
        super( props )
        //TODO handle what happens if this page is loaded w/o controller + group
        this.state = {
            searchResults: {'tracks':[]},
            recommendationResults: [],
            queue: [],
            query: '',
            group: this.props.location.group || ''
        }
        this.searchHandler = this.searchHandler.bind(this)
        this.addToQueueHandler = this.addToQueueHandler.bind(this)
        this.handleNext = this.handleNext.bind(this)
        this.handlePause = this.handlePause.bind(this)
        this.handlePlay = this.handlePlay.bind(this)
        this.handleSeek = this.handleSeek.bind(this)

        this.controller = new ControllerInterface()
        
    }

    createGroup = async () => {
        this.props.dispatch(startController())
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
        if (this.props.user.isLoggedIn) {
            this.createGroup()
        }
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

    addToQueueHandler = async (songUri) => {
      console.log('adding ' + songUri + ' to queue.')
      const success = await this.controller.add(songUri)
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

    clearSearchResults = () => {
        this.state.searchResults = {'tracks': []}
    }

    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'play');
    }

    render() {
        const searchHeaders = ['', 'title', 'artists', 'album', 'Add']
        const queueHeaders = ['', 'title', 'artists', 'album', 'Remove']

        return (
            <React.Fragment>
                <Card style={{ width: '18rem' }}>
                    <Card.Body>
                        <Card.Text style={{color: 'black'}}>
                            Group: {this.props.controller.group}
                        </Card.Text>
                    </Card.Body>
                </Card>
                <main className="main-area">
                    <Container className="col-container">
                        <Row>
                            <Col className="search-container">
                                <h2>Search Results</h2>
                                <SearchBar setSearchResults={this.searchHandler} />
                                <SongTable
                                    songs={this.state.searchResults.tracks}
                                    handleAdd={this.addToQueueHandler}
                                    actionName={'Add'}
                                    header={searchHeaders}/>
                            </Col>
                            <Col className="controller-queue-container">
                                <h2>Current Queue</h2>
                                <SongTable
                                songs={this.state.queue}
                                handleAdd={this.removeFromQueueHandler}
                                actionName={'Remove'}
                                header={queueHeaders}/>
                                <Row>
                                    <Col className="button-col">
                                        <Button
                                            key={uuid()}
                                            className="button"
                                            onClick={this.handlePlay}>
                                            PLAY
                                        </Button>
                                        <Button
                                            key={uuid()}
                                            className="button"
                                            onClick={this.handleNext}>
                                            NEXT
                                        </Button>
                                    </Col>
                                </Row>
                            </Col>


                        </Row>

                    </Container>

                </main>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(Controller));