import React from 'react';
import {connect} from 'react-redux';
import {getCurrentSong} from "../../actions/actions.js";
import {withSongPolling} from "./withSongPolling";
import {Button, Card} from 'react-bootstrap'

//TODO figure out additional display info like track features, popularity, release date, etc.
//key energy danceability valence
//Progress bar during song?
class CurrentSongCard extends React.Component {
  //TODO make this body a SongCard that can be reusable separately from ths polling Card
  constructor (props) {
    super(props)
  }

  render() {
    if (this.props.song.name) {
      this.doRender = true
      this.title = this.props.song.name
      this.artists = this.props.song.artists.map((a) => (a.name)).join()
      this.album = this.props.song.album && this.props.song.album.name
      this.imageSrc = this.props.song.images["lg"].url
    }
    if (this.doRender) {
        return (<Card bg="primary" className="text-center" style={{ width: '18rem' }}>
          <Card.Body>
            <Card.Img variant="top" src={this.imageSrc} />
            <Card.Title>{this.title}</Card.Title>
            <Card.Text>
              {this.artists}
            </Card.Text>
            <Card.Text className="text-muted" >
              {this.album}
            </Card.Text>
          </Card.Body>
        </Card>)
    } else {
      return (
          <Card.Body>
            <Card.Text className="text-muted">
              This room does not have any songs playing right now.
            </Card.Text>
          </Card.Body>
      )
    }
  }
}

const mapStateToProps = state => ({
    // currentSong: state.listener.currentSong
});
const mapDispatchToProps = {};
export default CurrentSongCard
//Was used for song to poll for itself.
// export default withSongPolling(getCurrentSong)(
//     connect(mapStateToProps, mapDispatchToProps)(CurrentSongCard)
//   );