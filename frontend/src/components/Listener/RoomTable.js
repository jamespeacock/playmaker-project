import React from "react";
import {Link} from "react-router-dom";
import PropTypes from "prop-types";

export default class RoomTable extends React.Component {
    //TODO make this body a SongCard that can be reusable separately from ths polling Card
    constructor (props) {
        super(props)
    }

    handlePlay = async () => {
        this.props.history.push({
            pathname: '/play',
            mode: 'curate'
        })
    }

    renderTableData() {
        return this.props.rooms.map((room, index) => {
            const name = room.name
            const currentSong = room.current_song.name
            const numListeners = room.listeners.length
            const imgUrl = room.current_song.images.sm.url
            const curator = room.controller
            const id = room.id

            return (
                <tr key={index} style={{width: '20rem'}}>
                    <td className="text-center"><img className="img-responsive"
                                                     src={imgUrl}/></td>
                    <td className="text-center">{name}</td>
                    <td className="text-center">{currentSong}</td>
                    <td className="text-center">{numListeners}</td>
                    <td className="text-center">{curator}</td>
                    {this.props.actionName && <td className="text-center">
                        <button type="button"
                                className="btn btn-primary"
                                onClick={() => this.props.actionHandler(id)}>
                            {this.props.actionName}
                        </button>
                    </td>}
                </tr>
            )
        })
    }

    renderTableHeader() {
        let header = ['', 'room name', 'now playing', 'listeners', 'curator', ''] //swap these out with icons
        //future: genre / vibes pie chart / viz tooltips
        return header.map((key, index) => {
            return <th className="text-center" key={index}>{key.toUpperCase()}</th>
        })
    }

    render() {
        if (this.props.rooms.length === 0) {
            return (<div>There are no rooms available to join. :( You can create one <Link to={'play'}>here</Link></div>)
        }
        return (
            <div>
                <table id='tracks'>
                    <tbody>
                    <tr>{this.renderTableHeader()}</tr>
                    {this.renderTableData()}
                    </tbody>
                </table>
            </div>
        )
    }
}

RoomTable.propTypes = {
    actionHandler: PropTypes.func.isRequired,
    actionName: PropTypes.string,
    rooms: PropTypes.array
}
