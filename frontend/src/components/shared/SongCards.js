import React from 'react';
import {Card} from 'react-bootstrap'
import AppContext from '../AppContext'

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
        return (<Card>
          <Card.Body className="card-song">
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
          <AppContext.Consumer>
            {
              ({user}) =>
              <Card.Body>
                  {this.props.isController ?
                      <Card.Text className="text-muted">You're not playing a song! Start playing in <a href="https://www.spotify.com/us/redirect/webplayerlink/" target="_blank">Spotify</a>. If you are playing a song, try <a href={user.auth_url}>refreshing.</a></Card.Text>:
                      <Card.Text className="text-muted">This room does not have any songs playing right now.</Card.Text>}
              </Card.Body>
            }
          </AppContext.Consumer>
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