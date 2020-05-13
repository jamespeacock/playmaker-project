import React  from 'react';
import { render } from 'react-dom'
import { BrowserRouter as Router } from 'react-router-dom';
// import './index.css';
//import 'bootstrap/dist/css/bootstrap.min.css';
import './custom.scss';
import Root from './Root';

render(
    <Root />,
    document.getElementById('root')
)
