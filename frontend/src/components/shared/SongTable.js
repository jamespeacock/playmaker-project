import React from 'react'
import Button from 'react-bootstrap/Button'
import BootstrapTable from 'react-bootstrap-table-next';
import '../../../node_modules/react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'

function buttonFormatter(cell, row){
  return (<Button type="submit" onClick={ console.log("clicked") }></Button>);
}


const columns = [{
  dataField: 'uri',
  text: '',
  hidden: true
},{
  dataField: 'name',
  text: 'Song Title'
}, {
  dataField: 'artists',
  text: 'Artists'
}];

const columnsWithButton = [{
  dataField: 'uri',
  text: '',
  hidden: true
},{
  dataField: 'name',
  text: 'Song Title'
}, {
  dataField: 'artists',
  text: 'Artists'
},{
  dataField: 'add',
  text: 'Add',
  dataFormat: buttonFormatter
}];

function songView(song) {
  var songRow = Object.assign({}, song);
  songRow.artists = songRow.artists.map((a) => (a.name)).join()
  return songRow
}

export default class SongTable extends React.Component {
    constructor( props ) {
      super(props)
    }

    componentDidMount() {
    }

    render() {
      return (
          <div>
              <BootstrapTable
                keyField="uri"
                data={this.props.songs.map(songView)}
                columns={ (this.props.withButtons) ? columnsWithButton :columns }/>
                <p>{this.props.isFetching ? 'Fetching queue...' : ''}</p>
          </div>
      )
    }
}