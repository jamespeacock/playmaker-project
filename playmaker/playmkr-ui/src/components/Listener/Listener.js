import React from 'react'
import ApiInterface from '../../API/ApiInterface'
import Header from '../Header/Header'
import './listener.css'
const uuid = require('uuid/v4')

export default class Listener extends React.Component {

    constructor( props ) {
        super( props )
        this.state = {
            songsList: []
        }
    }
    componentDidMount() {
        this.getSongsInterface()
    }

    getSongsInterface = async ( ) => {
        this.songsInterface = new ApiInterface( {
            method : 'GET', 
            endpoint : 'controller/queue'
        } )
        const songsList = await this.songsInterface.goFetch()
        this.setState( { songsList } )
    }

    nextInterface = async ( ) => {
        this.songsInterface = new ApiInterface( {
            method : 'GET', 
            endpoint : '/controller/next'
        } )
        const songsList = await this.songsInterface.goFetch()
        this.setState( { songsList } )
    }

    pauseInterface = async ( ) => {
        this.songsInterface = new ApiInterface( {
            method : 'GET', 
            endpoint : '/controller/pause'
        } )
        const songsList = await this.songsInterface.goFetch()
        this.setState( { songsList } )
    }

    playInterface = async ( ) => {
        this.songsInterface = new ApiInterface( {
            method : 'GET', 
            endpoint : '/controller/play'
        } )
        const songsList = await this.songsInterface.goFetch()
        this.setState( { songsList } )
    }
    
    seekInterface = async ( ) => {
        this.songsInterface = new ApiInterface( {
            method : 'GET', 
            endpoint : '/controller/seek'
        } )
        const songsList = await this.songsInterface.goFetch()
        this.setState( { songsList } )
    }

    handleNext= () => {
        console.log('next')
        this.handleNext()
    }

    handlePause= () => {
        console.log('pause')
        this.handlePause()
    }

    handlePlay = () => {
        console.log('play')
        this.handlePlay()
    }

    handleSeek = () => {
        console.log('seek')
        this.handleSeek()
    }

    render() {
        const { songsList } = this.state
        // console.log('rendering listener')
        const sampleData = [
            { 
                name: 'POP SEMI', 
                artists: ['pax osa']
            }, 
            { 
                name: 'SHOOTING STARS', 
                artists: ['the bag raiders']
            },
            { 
                name: 'SENIORITA', 
                artists: ['shawn mendez']
            }
        ]

        return (
            <React.Fragment>
                <Header></Header>
                <main className="listener-area">
                    <section className="listener-queue-container">
                        <h2 className="listener-queue-title">Listening Queue</h2>
                        <ul className="listener-queue-list">
                            {sampleData.length && sampleData.map( song => (<li className="listener-queue-item"> {song.name} <br></br> {song.artists[0]}</li>))}
                        </ul>
                        <div className="button-container">
                            <div className="button-col-left">
                                <button 
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handlePlay}>
                                    PLAY
                                </button>
                                <button 
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handleSeek}>
                                    SEEK
                                </button>
                            </div>
                            <div className="button-col-right">
                                <button 
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handleNext}>
                                    NEXT
                                </button>
                                <button 
                                    key={uuid()}
                                    className="button"
                                    onClick={this.handlePause}>
                                    PAUSE
                                </button>
                            </div>
                        </div>
                    </section>
                </main>
            </React.Fragment>
        )
    }
}
