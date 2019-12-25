import * as React from 'react';
import {connect} from 'react-redux';

export const withSongPolling = (currentSongAction, duration = 50000) => Component => {
    const SongCardWrapper = () => (
        class extends React.Component {
            componentDidMount() {
                this.props.currentSongAction();
                this.songPolling = setInterval(
                    () => {
                        this.props.currentSongAction();
                    },
                    duration);
            }
            componentWillUnmount() {
                clearInterval(this.songPolling);
            }
            render() {
                console.log("props from currentSong to SongCard", this.props)
                return <Component {...this.props}/>;
            }
        });
    const mapStateToProps = () => ({});
    const mapDispatchToProps = {currentSongAction};
    return connect(mapStateToProps, mapDispatchToProps)(SongCardWrapper())
};