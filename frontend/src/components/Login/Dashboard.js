import React from 'react'
import { withRouter } from 'react-router-dom'
import {Button, Container, Row, Col, Jumbotron} from 'react-bootstrap'
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import {connect} from "react-redux";
import './dashboard.css';

class Dashboard extends React.Component {

    constructor ( props ) {
        super(props)
    }

    handlePlay = async (mode) => {
        this.props.history.push({
          pathname: '/play',
          mode: mode
        })
    }

    handleListen = async () => {
        this.props.history.push({
          pathname: '/listen'
        })
    }

    componentWillMount() {
        //If in a room already, route them there.
        if (this.props.user.isController && this.props.controller.room) {
            this.props.history.push('/play')
        } else if (this.props.user.isListener && this.props.listener.isInRoom ) {
            this.props.history.push('/listen/'+ this.props.listener.room.id)
        } else if (this.props.user.isListener) {
            this.props.history.push('/listen')
        }
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force redirect after logout
        return (
          <React.Fragment>
              <Container lg={8} md={6}>
                  <Jumbotron className="jumbotron-dashboard">
                      <h1>listen with friends</h1>
                      <p>sync your spotify stream from any genre of room</p>
                      <Button
                          color={"dark"}
                          onClick={this.handleListen}>
                          browse rooms
                      </Button>
                  </Jumbotron>
                  <Jumbotron className="jumbotron-dashboard">
                      <h1>share your music</h1>
                      <p>broadcast your listening session for others to hear</p>
                      <Button
                          onClick={() => this.handlePlay('broadcast')}>
                          create a room
                      </Button>
                  </Jumbotron>
                  <Jumbotron className="jumbotron-dashboard">
                      <h1>curate a live set</h1>
                      <p>create a queue, see suggested songs, see listener's reactions</p>
                      <Button
                          onClick={() => this.handlePlay('curate')}>
                          create a curate room
                      </Button>
                  </Jumbotron>
              </Container>
          </React.Fragment>
        )
    }
}

export default withRouter(connect()(Dashboard));