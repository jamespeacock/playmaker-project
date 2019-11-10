import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
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
        const path = 'listener/join?group=' + group
        const resp = await new ApiInterface({}).get(path)
        if (resp && resp.group) {
            const action = startListener(resp.group, resp.songs)
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
        if (this.props.listener) {
            console.log(this.props.listener)
        }
        const willOpenGroupModal = !(this.props.user.isListener && this.props.listener.group && this.props.listener.group != '')
        return (
            <AppContext.Consumer>
                {() =>
                    <React.Fragment>
                        <Header></Header>
                        <main className="listener-area">
                            <section className="listener-queue-container">
                                <h2 className="listener-queue-title">Listening Queue</h2>
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