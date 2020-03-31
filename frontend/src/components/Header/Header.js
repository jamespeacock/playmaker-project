import React from 'react'
import logo from '../../assets/logo.png'
import { Navbar, NavDropdown, Image, Col } from 'react-bootstrap'
import AppContext from '../AppContext'
import {openDevices, openReport, openJoinRoom} from "../../actions/sessionActions";
import {startListener} from "../../actions/actions";
import {ShowDevicesModal} from "../shared/Devices";
import {connect} from "react-redux";
import FindRoomModal from "../rooms/FindRoomModal";
import SubmitReport from "../feedback/SubmitReport";

class Header extends React.Component {

    constructor (props) {
        super(props)

        this.state = {
            bg : 'green'
        }
    }

    render() {
        return (
        <AppContext.Consumer>
            {({logout}) =>
                <React.Fragment>
                    <Navbar bg={this.state.bg} expand="lg">
                        <Navbar.Brand href="#home">
                            <Col xs={4} md={3}>
                                <Image src={logo} fluid/>
                            </Col>
                        </Navbar.Brand>
                        <Col xs={4} md={3}>
                            <Navbar.Text>playmkr</Navbar.Text>
                        </Col>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        {this.props.user.isLoggedIn &&
                            <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                                <NavDropdown title={this.props.user.username + "'s Account"} id="basic-nav-dropdown" className="dropdown-menu-right">
                                    {this.props.user.isListener &&
                                    <NavDropdown.Item onClick={() =>
                                        this.props.dispatch(openJoinRoom())
                                    }>Direct Join</NavDropdown.Item>}
                                    <NavDropdown.Item onClick={() =>
                                        this.props.dispatch(openDevices())
                                    }>Devices</NavDropdown.Item>
                                    <NavDropdown.Divider/>
                                    <NavDropdown.Item href={this.props.user.auth_url}>Reauthenticate</NavDropdown.Item>
                                    <NavDropdown.Item onClick={ () =>
                                        this.props.dispatch(openReport())
                                    }>Report a Problem</NavDropdown.Item>
                                    <NavDropdown.Divider/>
                                    <NavDropdown.Item onClick={logout}>Log Out</NavDropdown.Item>
                                </NavDropdown>
                            </Navbar.Collapse>
                        }
                    </Navbar>
                {/*modals here*/}
                {this.props.session.showDevices && <ShowDevicesModal
                                                    user={this.props.user}/>}
                {this.props.session.showReport && <SubmitReport/>}
                {this.props.session.showJoinRoom && <FindRoomModal
                    joinRoom={(room) => this.props.dispatch(startListener(room))}
                    />}
                </React.Fragment>
            }
        </AppContext.Consumer>
        )
    }
}

export default connect()(Header)