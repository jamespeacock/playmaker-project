import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { debounce } from "throttle-debounce";
import SongTable from '../shared/SongTable'
import {Card} from "react-bootstrap";
import {connect} from "react-redux";
import {updateMode, refreshQueue, startController, editQueue, nextSong} from "../../actions/actions";
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import SongsInterface from "../../api/SongsInterface";


const uuid = require('uuid/v4')

class Controller extends React.Component {

    constructor( props ) {
        super( props )
        //TODO handle what happens if this page is loaded w/o controller + group
        this.state = {
            searchResults: {'tracks':[]},
            recommendationResults: [],
            query: '',
            mode: 'brodcast',
            searchFetching: false,
            queueFetching: false,
        }
        // this.addToQueueHandler = this.addToQueueHandler.bind(this)
        // this.handleNext = this.handleNext.bind(this)
        // this.handlePlay = this.handlePlay.bind(this)
        // this.handleSeek = this.handleSeek.bind(this)
        // this.SearchBar = this.SearchBar.bind(this)
        // this.changeMode = this.changeMode.bind(this)
        this.searchThrottled = debounce(500, this.search);
        this.songsInterface = new SongsInterface( {})
        
    }

    createGroup = async () => {
        this.props.dispatch(startController())
    }

    async changeMode( ) {
        if ('broadcast' === this.state.mode) {
            this.setState({mode: 'curate'});
        } else {
            this.setState({mode: 'broadcast'})
        }
        this.props.dispatch(updateMode(this.state.mode))
    }

    async handleNext() {
      this.props.dispatch(nextSong(()=>this.setState({queueFetching:false})))
    }

    handleSeek( position ) {
        // this.controller.seek(position)
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn) {
            this.createGroup()
        }
    }

    search = async ( q ) => {
        this.setState({ searchFetching: true })
        //dispatch update search results
        const searchResults = await this.songsInterface.search(q)
        if (q === this.waitingFor) {
            this.setState({searchResults})
            this.setState({ searchFetching: false })
        }
    }

    trySearch = event => {
        this.setState( { q:event.target.value },() => {
            if (this.state.q.length > 0) {
                this.waitingFor = this.state.q;
                this.searchThrottled(this.state.q)
            }
        } )
    }

    SearchBar = () => {
        return (
            <div>
                <React.Fragment>
                    <InputGroup className="mb-2">
                        <FormControl
                            type="text"
                            name="query"
                            className="input-left"
                            placeholder="Search tracks"
                            required
                            onChange={this.trySearch}
                            aria-label="Search tracks"
                            aria-describedby="basic-addon2"
                        />
                    </InputGroup>
                </React.Fragment>
            </div>
        )
    }

    changeOrderHandler = async (songUri, oldPosition, newPosition) => {

    }

    refreshQueue = async ( ) => {
        this.setState({queueFetching: true})
        this.props.dispatch(refreshQueue('controller', () => this.setState({queueFetching: false})))
    }

    addToQueueHandler = async (songUri) => {
        this.setState({queueFetching: true})
        this.props.dispatch(editQueue(songUri, ()=>this.setState({queueFetching:false})))
    }

    removeFromQueueHandler = async (uri, position) => {
        this.setState({queueFetching: true})
        this.props.dispatch(editQueue(uri,()=>this.setState({queueFetching:false}), position, true))
    }

    clearSearchResults = () => {
        this.state.searchResults = {'tracks': []}
    }

    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'play');
        this.refreshQueue();
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
                                {this.SearchBar()}
                                <SongTable
                                    songs={this.state.searchResults.tracks}
                                    handleAction={this.addToQueueHandler}
                                    actionName={'Add'}
                                    header={searchHeaders}
                                    fetching={this.state.searchFetching}/>
                            </Col>
                            <Col className="controller-queue-container">
                                <h2>Current Queue</h2>
                                <SongTable
                                songs={this.props.controller.queue}
                                handleAction={this.removeFromQueueHandler}
                                actionName={'Remove'}
                                header={queueHeaders}
                                fetching={this.state.queueFetching}/>
                                <Row>
                                    <Col className="button-col">
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