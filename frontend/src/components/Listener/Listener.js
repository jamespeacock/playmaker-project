import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import {Redirect, withRouter} from "react-router-dom";
import AppContext from "../AppContext";
import {showDevicesModal, showJoinRoomModal, handleRedirectsIfNotLoggedInOrAuthed, showPlaying} from "../shared/utils";
import {connect} from "react-redux";
import {refreshQueue, startListener} from "../../actions/actions";
import Spinner from "react-bootstrap/Spinner";
import Container from "react-bootstrap/Container";
import {Card} from "react-bootstrap";

class Room extends React.Component {

    constructor( props ) {
        super( props )
        this.listener = new ListenerInterface()
        this.state = {
            queueFetching: false
        }
    }

    refreshQueue = async () => {
        this.props.dispatch(refreshQueue('listener', () => this.setState({queueFetching: false })))
    }


    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'listen');
        if (this.props.listener.room) {
            this.props.dispatch(startListener(this.props.listener.room))
            this.queuePolling = setInterval(
                () => {
                    this.refreshQueue();
                },
                10000);
        }
    }

    componentWillUnmount() {
        clearInterval(this.queuePolling);
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force redirect after logout
        let willOpenRoomModal = !(this.props.user.isListener && this.props.listener.room && '' !== this.props.listener.room)
        let willOpenDevicesModal = (!willOpenRoomModal && this.props.user.isLoggedIn && !this.props.user.active_device)
        if (this.props.listener.room && this.props.listener.roomClosed) {
            //TODO Redirect to room selection page in the future
            clearInterval(this.queuePolling);
            return <Redirect to={'dashboard'}/>
        }
        return (
            <AppContext.Consumer>
                {() =>
                    <React.Fragment>
                        <Card style={{ width: '18rem' }}>
                            <Card.Body>
                                <Card.Text style={{color: 'black'}}>
                                    Room: {this.props.listener.room.name || this.props.listener.room.id}
                                </Card.Text>
                            </Card.Body>
                        </Card>
                        <main className="listener-area">
                            <Container className="listener-queue-container">
                                {!this.state.queueFetching ?
                                    showPlaying(this.props.listener.currentSong, this.props.listener.queue) :
                                    <Spinner animation="border" variant="primary" />
                                }
                            </Container>
                            <Container>
                                Chat room coming soon!
                            </Container>
                        </main>
                        {showDevicesModal(this.props.user, willOpenDevicesModal )}
                        {showJoinRoomModal(this.findRoom, willOpenRoomModal)}
                    </React.Fragment>
                }
            </AppContext.Consumer>
        )
    }
}

export default withRouter(connect()(Room))