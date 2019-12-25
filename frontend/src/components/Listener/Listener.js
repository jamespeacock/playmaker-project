import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import CurrentSongCard from '../shared/SongCards'
import SongTable from '../shared/SongTable'
import Header from '../Header/Header'
import {Redirect, withRouter} from "react-router-dom";
import AppContext from "../AppContext";
import {showDevicesModal, showJoinGroupModal} from "../shared/utils";
import {connect} from "react-redux";
import {checkLoggedIn, startListener} from "../../actions/actions";
import ApiInterface from "../../api/ApiInterface";

class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.listener = new ListenerInterface()
        console.log('listener props', this.props)
        //Should props = listener aka this.props.listener -- this.props
        // this.props.listener.currentSong = {
        //   title: "Roses - Imanbek Remix",
        //   artists: "SAINt JHN, Imanbek",
        //   album: "album",
        //   imageSrc: "https://i.scdn.co/image/4c875b4b6f8b9c9130f8e35e48342fc61a43ff59"
        // }
    }

    // componentDidMount() {
    //     if (this.state.group) {
    //         console.log('calling refresh')
    //         this.getAndLoadSongs()
    //     } else {
    //         console.log('no group yet')
    //     }
    // }

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

    // getAndLoadSongs = async ( ) => {
    //     const songs = await this.listener.queue()
    //     this.setState( { songs: songs } )
    // }

    render() {
        if (!this.props.user.isLoggedIn) {
            this.props.history.push({
                pathname: '/login',
                redirect: 'listen'
            })
        }
        const willOpenGroupModal = !(this.props.user.isListener && this.props.listener.group && this.props.listener.group != '')
        return (
            <AppContext.Consumer>
                {() =>
                    <React.Fragment>
                        <main className="listener-area">
                            <section className="listener-queue-container">
                                <h2 className="listener-queue-title">Currently Playing</h2>
                                <CurrentSongCard
                                song={this.props.listener.currentSong}/>
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