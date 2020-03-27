import React from 'react'
import logo from '../../assets/logo.png'
import { Navbar, NavDropdown, Image, Col } from 'react-bootstrap'
import AppContext from '../AppContext'
import { showSubmitReportProblem, showDevicesModal } from '../shared/utils.js'

export default class Header extends React.Component {

    constructor (props) {

        // props.setShowDevices = setShowDevices
        super(props)
        this.state = {
            showDevices: false
        }


    }

    render() {
        return (
        <AppContext.Consumer>
            {({user, logout}) =>
                <React.Fragment>
                    <Navbar bg="light" expand="lg">
                        <Navbar.Brand href="#home">
                            <Col xs={4} md={3}>
                                <Image src={logo} fluid/>
                            </Col>
                        </Navbar.Brand>
                        <Col xs={4} md={3}>
                            <Navbar.Text>playmkr</Navbar.Text>
                        </Col>
                        {/*Move this somewhere legit lol.*/}
                        <Col xs={2} md={2}>
                            <Navbar.Text>{user.username}</Navbar.Text>
                        </Col>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        {user.isLoggedIn &&
                            <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                                <NavDropdown title="Account" id="basic-nav-dropdown">
                                    <NavDropdown.Item onClick={() => {
                                        this.setState({showDevices: true})
                                    }}>Devices</NavDropdown.Item>
                                    <NavDropdown.Item href={this.props.auth_url}>Reauthenticae</NavDropdown.Item>
                                    <NavDropdown.Divider/>
                                    <NavDropdown.Item onClick={showSubmitReportProblem}>Report a Problem</NavDropdown.Item>
                                    <NavDropdown.Item onClick={logout}>Log Out</NavDropdown.Item>
                                </NavDropdown>
                            </Navbar.Collapse>
                        }
                    </Navbar>
                {/*modals here*/}
                {showDevicesModal(user, this.state.showDevices)}
                </React.Fragment>
            }
        </AppContext.Consumer>
        )
    }
}