import React from "react";
import {Button} from "react-bootstrap";

export default class SongTable extends React.Component {
    //TODO make this body a SongCard that can be reusable separately from ths polling Card
    constructor (props) {
        super(props)
    }

    renderTableData() {
        console.log(this.props.songs)
        return this.props.songs.map((song, index) => {
            const title = song.name
            const artists = song.artists.map((a) => (a.name)).join()
            const album = song.album
            const imageSrc = song.images['sm']
            const uri = song.uriimages

            return (
                <tr key={index}>
                    <td className="text-center"><img className="img-responsive"
                                                     src={imageSrc}/></td>
                    <td className="text-center">{title}</td>
                    <td className="text-center">{artists}</td>
                    <td className="text-center">{album}</td>
                    {this.props.actionName && <td className="text-center">
                        <Button onClick={() => this.props.handleAction(uri, song.position)}>
                            {this.props.actionName}
                        </Button>
                    </td>}
                </tr>
            )
        })
    }

    renderTableHeader() {
        let header = ['', 'title', 'artists', 'album', '']
        return header.map((key, index) => {
            return <th className="text-center" key={index}>{key.toUpperCase()}</th>
        })
    }

    render() {
        if (this.props.songs.length === 0) {
            return (<div></div>)
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