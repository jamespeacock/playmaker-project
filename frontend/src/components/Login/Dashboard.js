import React from 'react'
import { withRouter } from 'react-router-dom'
import {Button, Container, Row, Col, Jumbotron} from 'react-bootstrap'
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import {fetchRooms} from "../../actions/actions";
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
        this.props.dispatch(fetchRooms())
        this.props.history.push({
          pathname: '/listen'
        })
    }

    componentWillMount() {
        //If in a room already, route them there.
        if (this.props.user.isController && this.props.controller.room) {
            this.props.history.push('/play')
        } else if (this.props.user.isListener && this.props.listener.room) {
            this.props.history.push('/listen/'+ this.props.listener.room.id)
        }
    }

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force redirect after logout
        return (
          <React.Fragment>
              <Container fluid>
                  <Jumbotron>
                      <Row md={4} sm={6}>
                          <Col>
                              <Button
                                  onClick={this.handleListen}>
                                  Listen with Friends
                              </Button>
                          </Col>
                      </Row>
                  </Jumbotron>
                  <Jumbotron>
                      <Row md={4} sm={6}>
                          <Col>
                              <Button
                                  onClick={() => this.handlePlay('broadcast')}>
                                  Broadcast your Vibes
                              </Button>
                          </Col>
                          <Col>
                              <Button
                                  onClick={() => this.handlePlay('curate')}>
                                  Curate a Set
                              </Button>
                          </Col>
                      </Row>
                  </Jumbotron>
              </Container>
          </React.Fragment>
        )
    }
}

export default withRouter(connect()(Dashboard));