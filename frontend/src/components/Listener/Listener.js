import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import CurrentSongCard from '../shared/SongCards'
import {Redirect, withRouter} from "react-router-dom";
import AppContext from "../AppContext";
import {showDevicesModal, showJoinGroupModal, handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import {connect} from "react-redux";
import {refreshQueue, startListener} from "../../actions/actions";
import SongTable from "../shared/SongTable";

class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.listener = new ListenerInterface()
        console.log('listener props', this.props)
    }


    findGroup = async (group) => {
        //TODO should I refactor to have api call in action?
        // dispatch(startListener(group))
        const resp = await new ListenerInterface({}).joinGroup(group)
        if (resp && resp.group) {
            const action = startListener(resp)
            this.props.dispatch(action)
            return true
        } else {
            return false
        }
    }

    refreshQueue = async () => {
        this.props.dispatch(refreshQueue('listener'))
    }


    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'listen');
        this.props.currentSongAction();
        this.queuePolling = setInterval(
            () => {
                this.refreshQueue();
            },
            50000);
    }

    componentWillUnmount() {
        clearInterval(this.queuePolling);
    }

    render() {
        const willOpenGroupModal = !(this.props.user.isListener && this.props.listener.group && '' !== this.props.listener.group)
        return (
            <AppContext.Consumer>
                {() =>
                    <React.Fragment>
                        <main className="listener-area">
                            <section className="listener-queue-container">
                                <h2 className="listener-queue-title">Currently Playing</h2>
                                {this.props.listener.currentSong.title && <CurrentSongCard song={this.props.listener.currentSong}/> }
                                <SongTable
                                    songs={this.props.listener.queue}
                                    headers={['', 'title', 'artists', 'album']}/>
                            </section>
                        </main>
                        {showDevicesModal(this.props.user, !willOpenGroupModal && this.props.user.isLoggedIn && !this.props.user.current_device && this.props.user.isListener )}
                        {showJoinGroupModal(this.findGroup, willOpenGroupModal)}
                    </React.Fragment>
                }
            </AppContext.Consumer>
        )
    }
}

export default withRouter(connect()(Listener))