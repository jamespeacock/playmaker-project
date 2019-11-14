import React, {useEffect} from 'react'
import {Button, Modal} from 'react-bootstrap'
import BootstrapTable from 'react-bootstrap-table-next';
import {refreshDevices, setDevice} from "../../actions/actions";
import {connect} from "react-redux";
import PropTypes from "prop-types";

class DevicesModal extends React.Component {
  
    constructor( props ) {
      super(props)
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

    buttonFormatter = (cell, row) => {
      return (<Button onClick={ () => {
          this.props.dispatch(setDevice(row));
          this.props.onHide();
      } }>Select</Button>);
    }


    render() {
      return (
          <Modal show={this.props.show} onHide={this.props.onHide}>
              <Modal.Header>
                  <Modal.Title style={{color:'black'}}>Your Listening Devices</Modal.Title>
              </Modal.Header>

              {this.props.user.current_device && <p>Currently listening on props.user.current_device.name</p>}

              <Modal.Body>
                  <p style={{color:'black'}}>Please select your listening device.</p>
                  <Button md={3} onClick={() => this.props.dispatch(refreshDevices())}>Refresh Devices</Button>
              </Modal.Body>

              <div>
                  <BootstrapTable
                      keyField="uri"
                      data={this.props.user.devices}
                      columns={this.columns}/>
              </div>
          </Modal>
      )
    }
}

DevicesModal.propTypes = {
    user: PropTypes.object.isRequired,
    dispatch: PropTypes.func.isRequired
}

const ConnectedDevicesModal = connect()(DevicesModal)

function ShowDevicesModal(props) {
    const [modalShow, setModalShow] = React.useState(props.initialShow);
    useEffect(() => {
        setModalShow(props.initialShow);
    }, [props])

    return(<ConnectedDevicesModal
        user={props.user}
        show={modalShow}
        onHide={() => setModalShow(false)}
    />)
};

export default ShowDevicesModal