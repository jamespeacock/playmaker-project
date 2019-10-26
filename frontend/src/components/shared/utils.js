import ShowDevicesModal from "./Devices";
import React from "react";
import {Button, Form, Modal} from "react-bootstrap";

const showSubmitReportProblem = () => {
    console.log("showing report.")
}

const showDevicesModal = (user, show) => {
    return (<ShowDevicesModal
        initialShow={show}
        user={user}/>)
}

const showJoinGroupModal = (findGroup, show) => {
    return (<ShowJoinGroupModal show={show}
                            findGroup={findGroup}/>)

};

function ShowJoinGroupModal(props) {
    const [modalShow, setModalShow] = React.useState(props.show);
    //TODO figure out proper setGroup or whatever passer. bc these two don't work !
    const [group, setGroup] = React.useState('');
    const [error, setError] = React.useState('');

    return(<JoinGroupModal
        show={modalShow}
        group={group}
        findGroup={props.findGroup}
        setGroup={setGroup}
        onHide = {() => setModalShow(false)}
        error = {error}
        setError={setError}
    />)
};

class JoinGroupModal extends React.Component {

    constructor (props) {
        super(props)
    }

    handleJoin = async () => {
        console.log("handle join: ", this.props)
        const success = await this.props.findGroup(this.props.group);
        if (success) {
            this.props.onHide()
        } else {
            this.props.setError('Sorry, that group does not exist.')
        }
    }

    render() {
        return (
            <Modal show={this.props.show} onHide={this.props.onHide}>
                <Form>
                    <Modal.Header>
                        <Modal.Title style={{color:'black'}}>Join a Group</Modal.Title>
                    </Modal.Header>
                    <Form.Group>
                        <Form.Control
                            type="text"
                            placeholder="shared room code"
                            onChange={(e) => this.props.setGroup(e.target.value)}
                            isInvalid={this.props.error}
                        />
                        <Form.Control.Feedback type='invalid'>{this.props.error}</Form.Control.Feedback>
                    </Form.Group>
                    <Button variant="primary" onClick={this.handleJoin}>
                        Join Group
                    </Button>
                </Form>
            </Modal>)
    }
}



export {
    showSubmitReportProblem,
    showDevicesModal,
    showJoinGroupModal
}

