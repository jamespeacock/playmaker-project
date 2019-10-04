import React from 'react'
import './header.css'
import logo from '../../assets/logo.png'
import { Navbar, NavDropdown, Image, Col } from 'react-bootstrap'
import AppContext from '../AppContext'

export default class Header extends React.Component {

    constructor (props) {
      super(props)
    }

    render() {
        return (
        <AppContext.Consumer>
            {({value}) =>
                <Navbar bg="light" expand="lg">
                    <Navbar.Brand href="#home">
                        <Col xs={4} md={3}>
                            <Image src={logo} fluid/>
                        </Col>
                    </Navbar.Brand>
                    <Col xs={4} md={3}>
                        <Navbar.Text>playmkr</Navbar.Text>
                    </Col>
                    <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                    <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                        <NavDropdown title="Account" id="basic-nav-dropdown">
                            <NavDropdown.Item href="#action/3.1">Go Listen</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.2">Go Curate</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">Settings</NavDropdown.Item>
                            <NavDropdown.Divider/>
                            <NavDropdown.Item onClick={value}>Log Out</NavDropdown.Item>
                        </NavDropdown>
                    </Navbar.Collapse>
                </Navbar>
            }
        </AppContext.Consumer>
        )
    }
}