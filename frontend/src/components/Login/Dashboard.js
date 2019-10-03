import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import {Form, FormControl, Button, Container} from 'react-bootstrap'
import Header from '../Header/Header'
import ApiInterface from '../../api/ApiInterface'
import './dashboard.css'
const uuid = require('uuid/v4')


class Dashboard extends React.Component {

    constructor ( props ) {
      super(props)
      this.state = {
          group : ''
      }
    }

    createGroup = async () => {
      var state = await new ApiInterface({}).get('controller/start')
      return state
    }

    findGroup = async () => {
      const path = 'listener/join?group=' + this.state.group
      var state = await new ApiInterface({}).get(path)
      return state
    }

    handlePlay = async () => {
        const { history } = this.props
        console.log('play')
        this.props.history.push({
          pathname: '/play',
          state: await this.createGroup()
        })
    }

    handleListen = async () => {
        const { history } = this.props
        history.push({
          pathname: '/listen',
          state: await this.findGroup()
        })
    }

    updateGroup = ( group ) => {
        this.setState( { group } )
    }

    render() {
        console.log('rendering dashboard')
        console.log(this.props.user.isLoggedIn)
        console.log(this.props.user)
        if (this.props.user.isLoggedIn) {
          return (
              <React.Fragment>
                  <Header></Header>
                  <Container>
                    <Form inline>
                      <FormControl 
                        type="text"
                        placeholder="shared listening code"
                        onChange={ keyInput => this.updateGroup( keyInput.target.value ) }
                        onSubmit={this.handleListen}/>
                      <Button>Join Room & Start Listening</Button>
                    </Form>
                
                    <Button
                        onClick={this.handlePlay}>
                        Curate for Others
                    </Button>
                  </Container>
              </React.Fragment>
          )
        }
        else {
          return <Redirect to='/login' />
        }
    }
}

export default withRouter(Dashboard);