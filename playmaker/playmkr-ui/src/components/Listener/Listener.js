import React from 'react'
import ApiInterface from '../../API/ApiInterface'
import Header from '../Header/Header'
import './listener.css'

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
            endpoint : '/controller/queue'
        } )
        const songsList = await this.songsInterface.goFetch()
        this.setState( { songsList } )
    }
    render() {
        const { songsList } = this.state
        console.log('rendering listener')
        const sampleData = [
            { 
                name: 'pop semi', 
                artists: ['pax osa']
            }, 
            { 
                name: 'old town road semi', 
                artists: ['naz x']
            }, 
            { 
                name: 'salvation', 
                artists: ['drake']
            }
        ]

        return (
            <React.Fragment>
                <Header></Header>
                <main className="listener-area">
                    <section className="listener-queue-container">
                        <h2 className="listener-queue-title">Listening Queue</h2>
                        <ul className="listener-queue-list">
                            {sampleData.length && sampleData.map( song => (<li className="listener-queue-item"> {`${song.name} by ${song.artists[0]}`}</li>))}
                        </ul>
                    </section>
                </main>
            </React.Fragment>
        )
    }
}