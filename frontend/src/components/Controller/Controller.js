import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { debounce } from "throttle-debounce";
import SongTable from '../shared/SongTable'
import {Card} from "react-bootstrap";
import {connect} from "react-redux";
import {updateMode, refreshQueue, startController, editQueue, nextSong} from "../../actions/actions";
import {handleRedirectsIfNotLoggedInOrAuthed, showPlaying} from "../shared/utils";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import SongsInterface from "../../api/SongsInterface";
import Spinner from "react-bootstrap/Spinner";


const uuid = require('uuid/v4')

class Controller extends React.Component {

    constructor( props ) {
        super( props )
        //TODO handle what happens if this page is loaded w/o controller + group
        this.state = {
            searchResults: {'tracks':[]},
            recommendationResults: [],
            query: '',
            mode: this.props.location.mode,
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

    createGroup = async ( mode ) => {
        //TODO figure out style for handling constants
        this.props.dispatch(startController(mode, 'curate' === mode ? this.refreshQueue : null))
    }

    async kickoffPoll () {
        this.queuePolling = setInterval(
            () => {
                this.refreshQueue();
            },
            50000);
    }

    async changeMode( ) {
        if ('broadcast' === this.state.mode) {
            this.setState({mode: 'curate'});
            this.kickoffPoll();
        } else {
            this.setState({mode: 'broadcast'})
        }
        this.props.dispatch(updateMode(this.state.mode))
    }

    async handleNext() {
      this.props.dispatch(nextSong(()=>this.setState({queueFetching:false})))
    }

    componentDidMount() {
        if (this.props.user.isLoggedIn) {
            this.createGroup(this.state.mode);
        }
    }

    search = async ( q ) => {
        this.setState({ searchFetching: true })
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
        })
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
        this.setState({queueFetching: 0 === this.props.controller.queue.length})
        this.props.dispatch(refreshQueue('controller', () => this.setState({queueFetching: false})))
    }

    addToQueueHandler = async (songUri) => {
        this.setState({queueFetching: 0 === this.props.controller.queue.length})
        this.props.dispatch(editQueue(songUri, ()=>this.setState({queueFetching:false})))
    }

    removeFromQueueHandler = async (uri, position) => {
        this.setState({queueFetching: 0 === this.props.controller.queue.length})
        this.props.dispatch(editQueue(uri,()=>this.setState({queueFetching:false}), position, true))
    }

    clearSearchResults = () => {
        this.state.searchResults = {'tracks': []}
    }

    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'play');
        this.kickoffPoll();
    }

    componentWillUnmount() {
        clearInterval(this.queuePolling);
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force logout


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
                            {'curate' === this.state.mode &&
                            <Col className="search-container">
                                <h2>Search Results</h2>
                                {this.SearchBar()}
                                {!this.state.searchFetching ? <SongTable
                                        songs={this.state.searchResults.tracks}
                                        handleAction={this.addToQueueHandler}
                                        actionName={'Add'}
                                    /> :
                                    <Spinner animation="border" variant="primary"/>
                                }
                            </Col>
                            }
                            <Col className="controller-queue-container">
                                {showPlaying(
                                    this.props.controller.currentSong,
                                    this.props.controller.queue,
                                    this.removeFromQueueHandler,
                                    'Remove')}
                                {this.props.controller.queue.length > 0 &&
                                    <Col className="button-col">
                                        <Button
                                            key={uuid()}
                                            className="button"
                                            onClick={this.handleNext}>
                                            NEXT
                                        </Button>
                                    </Col>
                                }
                            </Col>
                        </Row>
                    </Container>
                    <Container>
                        Live chat feed coming soon!
                    </Container>
                </main>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(Controller));