import React from 'react'
import Header from '../Header/Header'
import './controler.css'

export default class Controller extends React.Component {
    render() {
        console.log('rendering controller')
        return (
            <React.Fragment>
                <Header></Header>
                <main className="main-area">
                    <div className="col-container">
                        <section className="controller-queue-container">
                            <div className="col-title">Queue</div>
                            <ul>
                                <li>queue item</li>
                                <li>queue item</li>
                                <li>queue item</li>
                                <li>queue item</li>
                                <li>queue item</li>
                            </ul>
                        </section>

                        <section className="search-container">
                            <div className="col-title">Search</div>
                                <ul>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                    <li>search item</li>
                                </ul>
                        </section>

                        <section className="recommendations-container">
                            <div className="col-title">Listeners</div>
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