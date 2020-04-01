import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import AppContext from "../AppContext";
import {handleRedirectsIfNotLoggedInOrAuthed, showPlaying} from "../shared/utils";
import {connect} from "react-redux";
import {refreshQueue, startListener} from "../../actions/actions";
import Spinner from "react-bootstrap/Spinner";
import Container from "react-bootstrap/Container";
import {Card} from "react-bootstrap";
import {openDevices} from "../../actions/sessionActions";
import Button from "react-bootstrap/Button";
import {leaveRoom} from "../../actions/listenerActions";
import {Redirect, withRouter} from "react-router-dom";

class Room extends React.Component {

    constructor(props) {
        super(props)
        this.listener = new ListenerInterface()
        this.state = {
            queueFetching: false,
            roomFetching: true
        }
    }

    refreshQueue = async () => {
        this.setState({queuFetching: true})
        this.props.dispatch(refreshQueue('listener', () => this.setState({queueFetching: false})))
    }


    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'listen');
    }

    componentDidMount() {
        if (!this.isDeviceWorking()) {
            if (!this.props.session.showDevices ) { this.props.dispatch(openDevices()) }
        }
        let roomId = this.props.match && this.props.match.params ? this.props.match.params.id : '';
        if (roomId && this.state.roomFetching) {
            this.props.dispatch(startListener(roomId, () => this.setState({roomFetching: false})))
        }
    }


    componentWillUnmount() {
        clearInterval(this.queuePolling);
    }

    isDeviceWorking() {
        let room = this.props.listener.room
        let erredDevices = room && room.error && room.error.includes("Device")
        let isWorking = room.id && this.props.user.active_device && !erredDevices
        console.log("Is device working? ", isWorking, erredDevices, room.id)
        //If isWorking is undefined then it is true
        return isWorking != false
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, '/listen/'+this.props.listener.room.id);

        if ((!this.props.user.isListener || this.props.listener.roomClosed) && !this.state.roomFetching) {
            return (<Redirect to={'/listen'}/>)
        // } else if (this.state.roomFetching && (!this.props.listener.room || !this.props.listener.isInRoom || this.props.listener.roomClosed)) {
        //     clearInterval(this.queuePolling);
        //     console.log("Room is not ready yet.")
        //     return (<Spinner  animation="border" variant="primary"/>)
        } else if (!this.queuePolling) {
            console.log('Restarting queue polling')
            this.queuePolling = setInterval(
                () => {
                    this.refreshQueue();
                },
                10000);
        }
        return (
            <React.Fragment>
                <Container lg={8} md={6}>
                    <Card className="card-room" fluid>
                        <Card.Body>
                            <Card.Text style={{color: 'black'}}>
                                Room {this.props.listener.room.id}: {this.props.listener.room.name || ''}
                            </Card.Text>
                            <Button onClick={() => {
                                this.props.dispatch(leaveRoom())
                                clearInterval(this.queuePolling)
                            }}>Leave</Button>
                        </Card.Body>
                    </Card>
                    <main className="listener-area">
                        <Container className="listener-queue-container" fluid>
                            {!this.state.queueFetching ?
                                showPlaying(this.props.listener.currentSong, this.props.listener.queue) :
                                <Spinner animation="border" variant="primary"/>
                            }
                        </Container>
                        <Container>
                            Chat room coming soon!
                        </Container>
                    </main>
                </Container>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(Room))
