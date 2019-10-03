import React from 'react'
import Button from 'react-bootstrap/Button'
import BootstrapTable from 'react-bootstrap-table-next';
import '../../../node_modules/react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'

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
        text: 'Device Name'
      }, {
        dataField: 'type',
        text: 'Type'
      },{
        dataField: '',
        text: 'Select',
        id: 'select-button',
        formatter: this.buttonFormatter
      }];
    }

    componentDidMount() {}

    buttonFormatter = (cell, row) => {
      return (<Button onClick={ () => this.props.selectDeviceHandler(row) }>Select</Button>);
    }


    render() {
      return (
          <div>
              <BootstrapTable
                keyField="uri"
                data={this.props.devices}
                columns={ this.columns }/>
          </div>
      )
    }
}