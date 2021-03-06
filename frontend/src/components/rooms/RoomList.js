import React from 'react'
import {Redirect, withRouter} from 'react-router-dom'
import {Container} from 'react-bootstrap'
import {handleRedirectsIfNotLoggedInOrAuthed} from "../shared/utils";
import RoomTable from "../Listener/RoomTable";
import {connect} from "react-redux";

class RoomList extends React.Component {

    constructor ( props ) {
        super(props)
    }


    componentWillMount() {
        handleRedirectsIfNotLoggedInOrAuthed(this.props, '/listen'); //Here to force redirect after logout
    }

    render() {
        if (this.props.user.isInRoom && this.props.user.isListener && this.props.listener.room.id) {
            return(<Redirect to={'/listen/' + this.props.listener.room.id}/>)
        }
        return (
            <React.Fragment>
                <Container lg={8} md={6}>
                    <h2>Rooms</h2>
                    <RoomTable
                        rooms={this.props.rooms}
                        actionName={"Join"}
                        actionHandler={(id) => {
                            this.props.history.push({
                                pathname: '/listen/' + id
                            });
                        }}
                    >
                    </RoomTable>

                </Container>
            </React.Fragment>
        )
    }
}

export default withRouter(connect()(RoomList));