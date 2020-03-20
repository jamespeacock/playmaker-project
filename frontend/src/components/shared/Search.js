import { debounce } from "throttle-debounce";
import React from 'react'
import SongsInterface from '../../api/SongsInterface'
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";


export default class SearchBar extends React.Component {

  constructor ( props ) {
    super(props)
    this.searchThrottled = debounce(1000, this.search);
  }
  
  componentDidMount() {
      this.songsInterface = new SongsInterface( {})
  }



  render() {
    return (
        <div>
          <React.Fragment>
            <InputGroup className="mb-2">
              <FormControl
                  type="text"
                  name="query"
                  className="input-left"
                  placeholder="Search tracks"
                  required
                  onChange={this.props.changeQuery}
                  aria-label="Search tracks"
                  aria-describedby="basic-addon2"
              />
            </InputGroup>
          </React.Fragment>
        </div>
    )
  }
}