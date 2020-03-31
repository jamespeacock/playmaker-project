import React from "react";
import {Button} from "react-bootstrap";
import CurrentSongCard from "./SongCards";
import SongTable from "./SongTable";
const uuid = require('uuid/v4')

function handleRedirectsIfNotLoggedInOrAuthed(props, redirect, pathname='/login') {
    if (null === props.user.isLoggedIn || !props.user.isLoggedIn) {
        props.history.push({
            pathname,
            redirect
        })
    } else if (!props.user.is_authenticated) {
        console.log('logged in but not authenticated!');
        window.location.href = props.user.auth_url
    }
}


const showPlaying = (currentSong, queue, handleSkip, handleAction=null,  actionName='', isController=false) => {
        return (
            <div>
                <h2>Now Playing</h2>
                <CurrentSongCard song={currentSong} isController={isController}/>
                {queue.length > 0 && isController &&
                <Button
                    key={uuid()}
                    className="button"
                    onClick={handleSkip}>
                    SKIP
                </Button>
                }
                {queue.length > 0 && <h2>Up Next</h2> }
                <SongTable
                    songs={queue}
                    handleAction={handleAction}
                    actionName={actionName}/>
            </div>
        )
}


export {
    showPlaying,
    handleRedirectsIfNotLoggedInOrAuthed
}

