import React from 'react'
import './listener.css'

export default class Listener extends React.Component {
    render() {
        console.log('rendering listener')
        return (
            <React.Fragment>
                <header className="header-container">
                    <h2>play.mkr</h2>
                </header>
                <main className="listener-area">
                    <section className="queue-container">
                        <h2 className="queue-title">Listen Now</h2>
                        <div className="playing-now"> || Playing Now || </div>
                        <ul className="queue-list">
                            <li className="queue-item"> song </li>
                            <li className="queue-item"> song </li>
                            <li className="queue-item"> song </li>
                            <li className="queue-item"> song </li>
                            <li className="queue-item"> song </li>
                            <li className="queue-item"> song </li>
                        </ul>
                    </section>
                </main>
            </React.Fragment>
        )
    }
}