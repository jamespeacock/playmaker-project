import ShowDevicesModal from "./Devices";
import React from "react";

const showSubmitReportProblem = () => {
    console.log("showing report.")
}

const showDevicesModal = (user, show) => {
    return (<ShowDevicesModal
        initialShow={show}
        user={user}/>)
}



export {
    showSubmitReportProblem,
    showDevicesModal
}

