import React from 'react'
import ListenerInterface from '../../api/ListenerInterface'
import SongTable from '../shared/SongTable'
import Header from '../Header/Header'
import {Redirect, withRouter} from "react-router-dom";
import AppContext from "../AppContext";
import ApiInterface from "../../api/ApiInterface";
import {Button, Form} from "react-bootstrap";
import {showDevicesModal} from "../shared/utils";

class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            songs: [],
            group: ''
        }
        this.listener = new ListenerInterface()
    }

    componentDidMount() {
        if (this.state.group) {
            console.log('calling refresh')
            this.getAndLoadSongs()
        } else {
            console.log('no group yet')
            this.setState( { songs: [] } )
        }
    }

    componentWillMount() {
        if (!this.props.user.isLoggedIn) {
            this.props.history.push({
                pathname: '/login',
                redirect: '/listen'
            })
        }
    }

    findGroup = async () => {
        const path = 'listener/join?group=' + this.state.group
        const resp = await new ApiInterface({}).get(path)
        if (resp.songs) {
            this.setState({songs: resp.songs})
        }
    }

    getAndLoadSongs = async ( ) => {
        const songs = await this.listener.queue()
        this.setState( { songs: songs } )
    }

    updateGroup = ( group ) => {
        this.setState( { group } )
    }

    render() {
        return (
            <AppContext.Consumer>
                {() =>
                    <React.Fragment>
                        <Header></Header>
                        <Form>
                            <Form.Control
                                type="text"
                                placeholder="shared listening code"
                                onChange={this.updateGroup}
                            />
                            <Button variant="primary" type="submit" onClick={this.findGroup}>
                                Join Group
                            </Button>
                        </Form>
                        <main className="listener-area">
                            <section className="listener-queue-container">
                                <h2 className="listener-queue-title">Listening Queue</h2>
                                <SongTable
                                    songs={this.state.songs}
                                    withButtons={false}/>
                            </section>
                        </main>
                        {showDevicesModal(this.props.user, this.props.user.isLoggedIn ? this.props.user.devices.length === 0 : false)}
                    </React.Fragment>
                }
            </AppContext.Consumer>
        )
    }
}

export default withRouter(Listener)