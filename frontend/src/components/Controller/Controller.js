import React from 'react'
import {Redirect, withRouter} from 'react-router-dom'
import { debounce } from "throttle-debounce";
import SongTable from '../shared/SongTable'
import {Card} from "react-bootstrap";
import {connect} from "react-redux";
import {updateMode, refreshQueue, startController, editQueue, nextSong, playSong, setRoomName} from "../../actions/actions";
import {handleRedirectsIfNotLoggedInOrAuthed, showPlaying} from "../shared/utils";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import SongsInterface from "../../api/SongsInterface";
import Spinner from "react-bootstrap/Spinner";
import {openDevices} from "../../actions/sessionActions";
import {leaveRoom} from "../../actions/listenerActions";
import Button from "react-bootstrap/Button";
import {closeRoom} from "../../actions/controllerActions";
import styles from "../../App.scss";


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
            roomFetching: true
        }
        this.handleNext = this.handleNext.bind(this);
        this.searchThrottled = debounce(500, this.search);
        this.songsInterface = new SongsInterface( {})
        
    }

    createRoom = async ( mode ) => {
        //TODO figure out style for handling constants

    }

    kickoffPoll () {
        this.queuePolling = setInterval(
            () => {
                this.refreshQueue();
            },
            10000);
    }

    async changeMode( ) {
        if ('broadcast' === this.state.mode) {
            this.setState({mode: 'curate'});
        } else {
            this.setState({mode: 'broadcast'});
        }
        this.props.dispatch(updateMode(this.state.mode))
    }

    async handleNext() {
      this.props.dispatch(nextSong(()=>this.setState({queueFetching:false})))
    }

    componentDidMount() {
        if (this.props.user.isController || this.state.roomFetching) {
            this.props.dispatch(startController(this.state.mode || 'broadcast',
                () => {
                    this.setState({roomFetching: false});
                    if ('curate' === this.state.mode) {
                        this.refreshQueue()
                    }
                }))
            this.createRoom(this.state.mode || 'broadcast');
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

    SearchResults = () => {
        return !this.state.searchFetching ? //if not waiting on results
            <SongTable
                songs={this.state.searchResults.tracks}
                handleAction={this.props.controller.currentSong.name ? this.addToQueueHandler : this.playSongHandler}
                actionName={this.props.controller.currentSong.name ? 'Add' : 'Play'}
            /> : //else return "loading"
            <Spinner animation="border" variant="primary"/>

    }

    changeOrderHandler = async (songUri, oldPosition, newPosition) => {

    }

    refreshQueue = async ( ) => {
        this.setState({queueFetching: 0 === this.props.controller.queue.length})
        this.props.dispatch(refreshQueue('controller', () => this.setState({queueFetching: false})))
    }

    playSongHandler = async (uri)  =>{
        this.props.dispatch(playSong(uri))
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
        if (this.props.user.isLoggedIn && !this.props.user.active_device ) {
            this.props.dispatch(openDevices())
        }
        if (this.props.controller.room) {
            this.kickoffPoll();
        }
    }

    componentWillUnmount() {
        clearInterval(this.queuePolling);
    }

    keyPressed = (e) => {
        if (e.key === "Enter") {
            this.props.dispatch(setRoomName(this.props.controller.room.id, e.target.value))
        }
    }

    RoomCard = () => {
        let roomName = this.props.controller.room && this.props.controller.room.name;
        if (roomName && !this.state.editRoom) {
            return (<Card className={styles.card}>
                <Card.Body>
                    <Card.Text className={styles.cardText}>
                        Room Name: {this.props.controller.room.name}
                    </Card.Text>
                </Card.Body>
            </Card>)
        }
        return (
            <Card style={{width: '18rem'}}>
                <Card.Body>
                    <Card.Text style={{color: 'black'}}>
                        Room ID: {this.props.controller.room && this.props.controller.room.id}
                    </Card.Text>
                    <InputGroup className="mb-2">
                        <FormControl
                            type="text"
                            name="set-room-name"
                            className="input-left"
                            placeholder="Set Room Name"
                            required
                            onKeyPress={this.keyPressed}
                            aria-label="Save"
                            aria-describedby="basic-addon2"
                        />
                    </InputGroup>
                    <Button onClick={() => {
                        this.props.dispatch(closeRoom())
                        clearInterval(this.queuePolling)
                    }}>Close Room</Button>
                </Card.Body>
            </Card>
        );
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force logout
        if (!this.props.user.isController && !this.state.roomFetching) {
            return (<Redirect to={'/dashboard'}/>)
        }
        return (
            <React.Fragment>
                <main className="main-area">
                    <Container className="col-container">
                        <Row>
                            {this.RoomCard()}
                        </Row>
                        <Row>
                            {'curate' === this.state.mode &&
                            <Col className="search-container">
                                <h2>Search Results</h2>
                                {this.SearchBar()}
                                {this.SearchResults}
                            </Col>
                            }
                            <Col className="controller-queue-container">
                                <Row>
                                {showPlaying(
                                    this.props.controller.currentSong,
                                    this.props.controller.queue,
                                    this.handleNext,
                                    this.removeFromQueueHandler,
                                    'Remove',
                                    true)}
                                </Row>
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