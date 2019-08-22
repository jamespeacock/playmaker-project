import { debounce } from "throttle-debounce";
import React from 'react'
import SongsInterface from '../../api/SongsInterface'


export default class SearchBar extends React.Component {

  constructor ( props ) {
    super(props)
    this.searchThrottled = debounce(1000, this.search);
  }
  
  componentDidMount() {
      this.songsInterface = new SongsInterface( {

      })
  }

  search = async ( q ) => {
      const searchResults = await this.songsInterface.search(q)
      if (q == this.waitingFor) {
        this.props.setSearchResults( searchResults )
      }
  }

  changeQuery = event => {
    this.setState( { q:event.target.value },() => {
      if (this.state.q.length > 0) {
        this.waitingFor = this.state.q;
        this.searchThrottled(this.state.q)
      }
    } )
  }

  render() {
    return (
      <React.Fragment>
        <input  
            type="text" 
            name="query" 
            className="input-left"
            placeholder="Search"
            required
            onChange={this.changeQuery}>
        </input>
      </React.Fragment>
    )
  }
}