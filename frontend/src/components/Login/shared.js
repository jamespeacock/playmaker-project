import {Form} from "react-bootstrap";
import React from "react";

const loginHandleErrors  = ({ loginError }) => {
    return (
        <div>
            {loginError && <Form.Text>{loginError}</Form.Text>}
            {!loginError && <Form.Text>You'll be redirected to login to Spotify</Form.Text>}
        </div>
    );
};

const validateInput = (stateCallback) => {
    var errorMessage = "";
    stateCallback((prevState, props) => {
        return { loginError: errorMessage }
    })
}

export {
    loginHandleErrors,
    validateInput
}