import React from 'react'
import './controler.css'

export default class Controller extends React.Component {
    render() {
        console.log('rendering controller')
        return (
            <React.Fragment>
                <header class="header-container">
                    <h2>Controller Dashboard</h2>
                </header>
                <main class="main-area">
                    <div class="col-container">
                        <section class="queue-container">
                            <div class="col-title">Queue</div>
                            <ul>
                                <li>queue item</li>
                                <li>queue item</li>
                                <li>queue item</li>
                                <li>queue item</li>
                                <li>queue item</li>
                            </ul>
                        </section>

                        <section class="search-container">
                            <div class="col-title">Search</div>
                                <ul>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                </ul>
                        </section>

                        <section class="recommendations-container">
                            <div class="col-title">Listeners</div>
                                <ul>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                    <li>rec item</li>
                                </ul>
                        </section>
                    </div>
                </main>
            </React.Fragment>
        )
    }
}