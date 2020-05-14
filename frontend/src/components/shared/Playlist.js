import React from 'react'
import {Button, Card} from 'react-bootstrap'

const PlaylistButton = ({props}) => (
  <Button>
      props.buttonName    
  </Button>
);

const SongCard = ({props}) => (
  <Card style={{ width: '18rem' }}>
    <Card.Img variant="top" src="holder.js/100px180" />
    <Card.Body>
      <Card.Title>Song Name</Card.Title>
      <Card.Text>
        Artist Name
      </Card.Text>
      <Card.Text>
        Album Name
      </Card.Text>
      <Card.Text>
        {props.song}
      </Card.Text>
      <Button variant="primary">
        buttonComponent    
      </Button>
    </Card.Body>
  </Card>
);

class PlaylistCard extends React.Component {

  render() {
    const cardsArray = [1,2].map(song => (
      <SongCard song={song} />
    ));

    return (
      <div>
        {cardsArray}
      </div>
    );
  }
}

export {
  PlaylistCard
}