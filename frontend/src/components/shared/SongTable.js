import React from 'react'
import Button from 'react-bootstrap/Button'
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';

function songView(song) {
  var songRow = Object.assign({}, song);
  songRow.artists = songRow.artists.map((a) => (a.name)).join()
  return songRow
}

export default class SongTable extends React.Component {
  
    constructor( props ) {
      super(props)
      console.log(this.props)

      this.columns = [{
        dataField: 'uri',
        text: '',
        hidden: true
      },{
        dataField: 'name',
        text: 'Song Title'
      }, {
        dataField: 'artists',
        text: 'Artists'
      }]

      this.columnsWithButton = [{
        dataField: 'uri',
        text: '',
        hidden: true
      },{
        dataField: 'position',
        text: '',
        hidden: true
      },{
        dataField: 'name',
        text: 'Song Title'
      }, {
        dataField: 'artists',
        text: 'Artist'
      },{
        dataField: '',
        text: 'Add',
        id: 'add-button',
        formatter: this.addFormatter
      },{
        dataField: 'uri',
        text: 'Play',
        id: 'play-button',
        formatter: this.playFormatter
      }];
    }

    componentDidMount() {}

    addFormatter = (cell, row) => {
      return (<Button onClick={ () => this.props.handleAdd(row) }>{cell.text}</Button>);
    }

    playFormatter = (cell, row) => {
      return (<Button onClick={ () => this.props.handlePlay(row.uri) }>{cell.text}</Button>);
    }


    render() {
      //TODO get rid of bootstrap table it sucks. @Steven what are good tables
      return (
          <div>
              <BootstrapTable
                keyField="position"
                data={this.props.songs.map(songView)}
                columns={ (this.props.withButtons) ? this.columnsWithButton : this.columns }/>
          </div>
      )
    }
}