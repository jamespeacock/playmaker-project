import React from 'react'
import './header.css'
import logo from '../../assets/logo.jpg'

export default function Header( props ) {
    return (
        <header className="header-container">
            <image className="logo" alt="play.mkr logo" src={logo}></image>
        </header>
    )
}