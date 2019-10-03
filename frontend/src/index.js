import React  from 'react';
import { render } from 'react-dom'
import { BrowserRouter as Router } from 'react-router-dom';
import './index.css';
// import './spotify.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import Root from './Root';

render(
    <Root />,
    document.getElementById('root')
)
