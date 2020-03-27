import ShowDevicesModal from "./Devices";
import React, {useEffect} from "react";
import {Button, Form, Modal} from "react-bootstrap";
import CurrentSongCard from "./SongCards";
import SongTable from "./SongTable";
const uuid = require('uuid/v4')

function handleRedirectsIfNotLoggedInOrAuthed(props, redirect, pathname='/login') {
    if (null === props.user.isLoggedIn || !props.user.isLoggedIn) {
        props.history.push({
            pathname,
            redirect
        })
    } else if (!props.user.is_authenticated) {
        console.log('logged in but not authenticated!');
        window.location.href = props.user.auth_url
    }
}

const showSubmitReportProblem = () => {
    console.log("showing report.")
}

const showDevicesModal = (user, show) => {
    return (<ShowDevicesModal
        initialShow={show}
        user={user}/>)
}

const showJoinRoomModal = (findRoom, show) => {
    return (<ShowJoinRoomModal show={show}
                            findRoom={findRoom}/>)

};

const showPlaying = (currentSong, queue, handleSkip, handleAction=null,  actionName='', isController=false) => {
        return (
            <div>
                <h2>Now Playing</h2>
                <CurrentSongCard song={currentSong} isController={isController}/>
                {queue.length > 0 &&
                <Button
                    key={uuid()}
                    className="button"
                    onClick={handleSkip}>
                    SKIP
                </Button>
                }
                {queue.length > 0 && <h2>Up Next</h2> }
                <SongTable
                    songs={queue}
                    handleAction={handleAction}
                    actionName={actionName}/>
            </div>
        )
}

function ShowJoinRoomModal(props) {
    const [modalShow, setModalShow] = React.useState(props.show);
    useEffect(() => {
        setModalShow(props.show);
    }, [props])

    //Do I need use effect down here?
    const [room, setRoom] = React.useState('',);
    const [error, setError] = React.useState('');

    return(<JoinRoomModal
        show={modalShow}
        room={room}
        findRoom={props.findRoom}
        setRoom={setRoom}
        onHide = {() => setModalShow(false)}
        error = {error}
        setError={setError}
    />)
};

class JoinRoomModal extends React.Component {

    constructor (props) {
        super(props)
    }

    handleJoin = async () => {
        const success = await this.props.findRoom(this.props.room);
    }

    render() {
        return (
            <Modal show={this.props.show} onHide={this.props.onHide}>
                <Form>
                    <Modal.Header>
                        <Modal.Title style={{color:'black'}}>Join a Room</Modal.Title>
                    </Modal.Header>
                    <Form.Group>
                        <Form.Control
                            type="text"
                            placeholder="shared room code"
                            onChange={(e) => {
                                this.props.setError('')
                                this.props.setRoom(e.target.value)
                              }
                            }
                            isInvalid={this.props.error}
                        />
                        <Form.Control.Feedback type='invalid'>{this.props.error}</Form.Control.Feedback>
                    </Form.Group>
                    <Button variant="primary" onClick={this.handleJoin}>
                        Join Room
                    </Button>
                </Form>
            </Modal>)
    }
}



export {
    showSubmitReportProblem,
    showDevicesModal,
    showJoinRoomModal,
    showPlaying,
    handleRedirectsIfNotLoggedInOrAuthed
}

