import ShowDevicesModal from "./Devices";
import React, {useEffect} from "react";
import {Button, Form, Modal} from "react-bootstrap";

function handleRedirectsIfNotLoggedInOrAuthed(props, redirect, pathname='/login') {
    if (!props.user.isLoggedIn) {
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

const showJoinGroupModal = (findGroup, show) => {
    return (<ShowJoinGroupModal show={show}
                            findGroup={findGroup}/>)

};

function ShowJoinGroupModal(props) {
    const [modalShow, setModalShow] = React.useState(props.show);
    useEffect(() => {
        setModalShow(props.show);
    }, [props])

    //Do I need use effect down here?
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
                            onChange={(e) => {
                                this.props.setError('')
                                this.props.setGroup(e.target.value)
                              }
                            }
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
    showJoinGroupModal,
    handleRedirectsIfNotLoggedInOrAuthed
}

