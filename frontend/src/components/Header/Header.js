import React from 'react'
import logo from '../../assets/logo.png'
import { Navbar, NavDropdown, Image, Col, Row } from 'react-bootstrap'
import AppContext from '../AppContext'
import {openDevices, openReport, openJoinRoom} from "../../actions/sessionActions";
import {startListener} from "../../actions/actions";
import {ShowDevicesModal} from "../shared/Devices";
import {connect} from "react-redux";
import FindRoomModal from "../rooms/FindRoomModal";
import SubmitReport from "../feedback/SubmitReport";
import styles from '../../App.scss';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';

class Header extends React.Component {

    constructor (props) {
        super(props)

        this.state = {
            theme : "#3c763d" // can inject this via styles={{color:this.state.theme}}.
        }
    }

    render() {
        return (
        <AppContext.Consumer>
            {({logout}) =>
                <React.Fragment>
                    <Navbar className="navbar-header" expand="lg" sticky={'top'}>
                        <Navbar.Brand href="/dashboard">
                            <h2>playmaker</h2>
                        </Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        {this.props.user.isLoggedIn &&
                            <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                                <NavDropdown class={styles.navbarHeader} title={<AccountCircleIcon> {this.props.user.username[0].toUpperCase()}>}</AccountCircleIcon>} id="basic-nav-dropdown" className="dropdown-menu-right">
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