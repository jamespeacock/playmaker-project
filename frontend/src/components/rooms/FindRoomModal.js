import React from "react";
import RoomInterface from "../../api/RoomInterface";
import {Button, Form, Modal} from "react-bootstrap";

class FindRoomModal extends React.Component {

    constructor (props) {
        super(props)
        this.state = {
            show: true,
            room: '',
            error: ''
        }
    }

    handleJoin = async ( ) => {
        const foundRoom = await new RoomInterface().getRoom(this.state.room);
        if (!foundRoom.id) {
            this.setState({error: "Room " + this.state.room + " does not exist."})
        } else {
            this.props.joinRoom(foundRoom.id)
        }
    }

    render() {
        return (
            <Modal show={this.state.show} onHide={() => this.setState({show: false})}>
                <Form>
                    <Modal.Header>
                        <Modal.Title style={{color:'black'}}>Join a Room</Modal.Title>
                    </Modal.Header>
                    <Form.Group>
                        <Form.Control
                            type="text"
                            placeholder="shared room code"
                            onChange={(e) => {
                                this.setState({error:''})
                                this.setState({room: e.target.value})
                            }}
                            isInvalid={this.state.error}
                        />
                        <Form.Control.Feedback type='invalid'>{this.state.error}</Form.Control.Feedback>
                    </Form.Group>
                    <Button variant="primary" onClick={this.handleJoin}>
                        Join Room
                    </Button>
                </Form>
            </Modal>)
    }
}

export default FindRoomModal
