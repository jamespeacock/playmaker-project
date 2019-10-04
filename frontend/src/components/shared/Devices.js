import React from 'react'
import {Button, Modal} from 'react-bootstrap'
import BootstrapTable from 'react-bootstrap-table-next';
import '../../../node_modules/react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'

class DevicesModal extends React.Component {
  
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
      return (<Button onClick={ () => {
          this.props.selectDeviceHandler(row)
          this.props.onHide();
      } }>Select</Button>);
    }


    render() {
      return (
          <Modal show={this.props.show} onHide={this.props.onHide}>
              <Modal.Header>
                  <Modal.Title style={{color:'black'}}>Your Listening Devices</Modal.Title>
              </Modal.Header>

              <Modal.Body>
                  <p style={{color:'black'}}>Please select your listening device.</p>
                  <Button md={3} onClick={this.refreshDevices}>Refresh Devices</Button>
              </Modal.Body>

              <div>
                  <BootstrapTable
                      keyField="uri"
                      data={this.props.devices}
                      columns={this.columns}/>
              </div>
          </Modal>
      )
    }
}

export default DevicesModal