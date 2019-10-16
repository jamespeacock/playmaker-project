import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import {Button, Container, Row, Col, Jumbotron} from 'react-bootstrap'


class Dashboard extends React.Component {

    constructor ( props ) {
      super(props)
    }

    handlePlay = async () => {
        this.props.history.push({
          pathname: '/play'
        })
    }

    handleListen = async () => {
        this.props.history.push({
          pathname: '/listen'
        })
    }

    render() {
      return (
          <React.Fragment>
              <Jumbotron>
                  <Container>
                      <Row>
                          <Col>
                              <Button
                                  onClick={this.handlePlay}>
                                  Curate for Others
                              </Button>
                          </Col>
                          <Col>
                              <Button
                                  onClick={this.handleListen}>
                                  Join Room & Start Listening
                              </Button>
                          </Col>
                      </Row>
                  </Container>
              </Jumbotron>
          </React.Fragment>
      )
    }
}

export default withRouter(Dashboard);