import React from 'react'
import { withRouter } from 'react-router-dom'
import {Button, Container, Row, Col} from 'react-bootstrap'
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";



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

    render() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force redirect after logout
        return (
          <React.Fragment>
                  <Container fluid>
                      <Row md={4} sm={6}>
                          <Col>
                              <Button
                                  onClick={this.handleListen}>
                                  Listen with Friends
                              </Button>
                          </Col>
                      </Row>
                      <br/>
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
                  </Container>
          </React.Fragment>
        )
    }
}

export default withRouter(Dashboard);