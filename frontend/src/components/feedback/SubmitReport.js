import {connect} from "react-redux";
import React from 'react'
import {Button, Form, Modal} from 'react-bootstrap'
import {submitReport} from "../../actions/actions";
import FormLabel from "react-bootstrap/FormLabel";


class SubmitReport extends React.Component {

    constructor (props) {
        super(props)
        this.state = {
            report: {
                isFeature: false,
                text: ''
            },
            show: true
        }
    }

    render() {
        return (
            <Modal show={this.state.show} onHide={() => this.setState({show: false})}>
                <Modal.Header>
                    <Modal.Title style={{color: 'black'}}>Report an Issue</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <p style={{color: 'black'}}>Please select the type of issue you encountered.</p>
                        <Form.Group>
                            <Form.Group check>
                                <FormLabel check>
                                    <Form.Control type="radio" name="radioIssue" onChange={()=>this.setState({report:{isFeature: false}})}>Report a Problem</Form.Control>
                                </FormLabel>
                            </Form.Group>
                            <Form.Group check>
                                <FormLabel check>
                                    <Form.Control type="radio" name="radioFeature" value="Request a Feature" onChange={()=>this.setState({report: {isFeature: true}})}>Request a Feature</Form.Control>
                                </FormLabel>
                            </Form.Group>
                        </Form.Group>
                        <Form.Group >
                            <FormLabel for="exampleText">{this.state.report.isFeature ? "Describe the Desired Feature" : "Describe the Issue Encountered"}
                            <Form.Control type="textarea" name="text" id="reportText" onChange={(e)=>this.setState({report:{text:e.target.value}})}/>
                            </FormLabel>
                        </Form.Group>
                        <Button md={3} onClick={() => this.props.dispatch(submitReport(this.state.report))}>Submit</Button>
                    </Form>
                </Modal.Body>
            </Modal>
        )
    }
}

export default connect()(SubmitReport)