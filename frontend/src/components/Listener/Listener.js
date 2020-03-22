import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import CurrentSongCard from '../shared/SongCards'
import {Redirect, withRouter} from "react-router-dom";
import AppContext from "../AppContext";
import {showDevicesModal, showJoinGroupModal, handleRedirectsIfNotLoggedInOrAuthed, showPlaying} from "../shared/utils";
import {connect} from "react-redux";
import {refreshQueue, startListener} from "../../actions/actions";
import SongTable from "../shared/SongTable";
import Spinner from "react-bootstrap/Spinner";
import Container from "react-bootstrap/Container";

class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.listener = new ListenerInterface()
        console.log('listener props', this.props)
        this.state = {
            queueFetching: false
        }
    }

    findGroup = async (group) => {
        this.props.dispatch(startListener(group))
    }

    refreshQueue = async () => {
        this.props.dispatch(refreshQueue('listener', () => this.setState({queueFetching: false })))
    }


    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'listen');
        // this.props.currentSongAction();
        this.setState({queueFetching: this.props.listener.queue && 0 === this.props.listener.queue.length})
        if (this.props.listener.group) {
            this.findGroup(this.props.listener.group);
            this.queuePolling = setInterval(
                () => {
                    this.refreshQueue();
                },
                5000);
        }
    }

    componentWillUnmount() {
        clearInterval(this.queuePolling);
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force redirect after logout
        let willOpenGroupModal = !(this.props.user.isListener && this.props.listener.group && '' !== this.props.listener.group)
        let willOpenDevicesModal = (!willOpenGroupModal && this.props.user.isLoggedIn && !this.props.user.active_device)
        console.log(!this.props.user.active_device)
        console.log(this.props.user.active_device)
        return (
            <AppContext.Consumer>
                {() =>
                    <React.Fragment>
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
                        {showJoinGroupModal(this.findGroup, willOpenGroupModal)}
                    </React.Fragment>
                }
            </AppContext.Consumer>
        )
    }
}

export default withRouter(connect()(Listener))