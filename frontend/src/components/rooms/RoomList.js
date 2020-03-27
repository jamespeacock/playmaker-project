import {startListener} from "../../actions/actions";

import React from 'react'
import { withRouter } from 'react-router-dom'
import {Container} from 'react-bootstrap'
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import RoomTable from "../Listener/RoomTable";
import {connect} from "react-redux";

class RoomList extends React.Component {

    constructor ( props ) {
        super(props)
    }

    handleListen = async () => {
        this.props.history.push({
            pathname: '/listen'
        })
    }

    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, 'login'); //Here to force redirect after logout
        if (this.props.user.isInRoom && this.props.user.isListener) {
            this.props.history.push({
                pathname: '/listen/' + this.props.user.room
            });
        }
    }

    render() {

        return (
            <React.Fragment>
                <Container fluid>
                    <h2>Rooms</h2>
                    <RoomTable
                        rooms={this.props.rooms || []}
                        actionName={"Join"}
                        actionHandler={(id) => this.props.dispatch(startListener(id))}
                    >
                    </RoomTable>

                </Container>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(RoomList));