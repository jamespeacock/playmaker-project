import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import CurrentSongCard from '../shared/SongCards'
import SongTable from '../shared/SongTableOld'
import {Redirect, withRouter} from "react-router-dom";
import AppContext from "../AppContext";
import {showDevicesModal, showJoinGroupModal, handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import {connect} from "react-redux";
import {startListener} from "../../actions/actions";

class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.listener = new ListenerInterface()
        console.log('listener props', this.props)
    }


    findGroup = async (group) => {
        const resp = await new ListenerInterface({}).joinGroup(group)
        if (resp && resp.group) {
            const action = startListener(resp)
            this.props.dispatch(action)
            return true
        } else {
            return false
        }
    }

    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'listen');
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
                                    withButtons={false}/>
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