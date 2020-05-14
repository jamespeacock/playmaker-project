import React from 'react'
import {Button, Modal} from 'react-bootstrap'
import BootstrapTable from 'react-bootstrap-table-next';
import {refreshDevices, setDevice} from "../../actions/actions";
import {connect} from "react-redux";
import PropTypes from "prop-types";

class DevicesModal extends React.Component {
  
    constructor( props ) {
      super(props)
      this.columns = [{
        dataField: 'sp_id',
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

      this.state = {
          show: true
      }
    }

    buttonFormatter = (cell, row) => {
      return (<Button onClick={ () => {
          this.props.dispatch(setDevice(row));
          this.setState({show: false});
      } }>Select</Button>);
    }

    currentDevice(device){
        if (device) {
            return (<p style={{color:'black'}}>Currently listening on {device.name}</p>)
        } else {
            return ''
        }
    }

    componentWillMount() {
        this.props.dispatch(refreshDevices())
    }


    render() {
      return (
          <Modal show={this.state.show} onHide={() => this.setState({show:false})}>
              <Modal.Header>
                  <Modal.Title style={{color:'black'}}>Your Listening Devices</Modal.Title>
              </Modal.Header>
              {this.currentDevice(this.props.user.active_device)}
              <Modal.Body>
                  <p style={{color:'black'}}>Please select your listening device.</p>
                  <Button md={3} onClick={() => this.props.dispatch(refreshDevices())}>Refresh Devices</Button>
              </Modal.Body>
              <div>
                  <BootstrapTable
                      keyField="sp_id"
                      data={this.props.user.devices}
                      columns={this.columns}/>
              </div>
              <p style={{color:'black'}}>Oddly, mobile devices do not appear unless they are open.</p>
          </Modal>
      )
    }
}

DevicesModal.propTypes = {
    user: PropTypes.object.isRequired,
    dispatch: PropTypes.func.isRequired
}

const ShowDevicesModal = connect()(DevicesModal)

export {
    ShowDevicesModal
}