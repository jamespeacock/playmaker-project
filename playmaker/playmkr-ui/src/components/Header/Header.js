import React from 'react'
import './header.css'
import logo from '../../assets/logo.png'

export default function Header( props ) {
    return (
        <header className="header-container">
            <img className="logo" alt="playmkr logo" src={logo}/>
        </header>
    )
}