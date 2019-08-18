import React from 'react'
import BootstrapTable from 'react-bootstrap-table-next';
import '../../../node_modules/react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'

const columns = [{
  dataField: 'id',
  text: 'Position'
},{
  dataField: 'name',
  text: 'Song Title'
}, {
  dataField: 'artists',
  text: 'Artists'
}];

export default class SongTable extends React.Component {
    constructor( props ) {
      console.log('in queue table constructor')
      console.log(props)
      super(props)
    }

    render() {

      return (
          <div>
              <BootstrapTable
                keyField="id"
                data={this.props.songs}
                columns={ columns }/>
              <p>{this.props.isFetching ? 'Fetching queue...' : ''}</p>
          </div>
      )
    }
}