package com.gwidgets.client.models;


import com.fasterxml.jackson.annotation.JsonIgnore;
import com.google.gwt.core.client.GWT;
import com.github.nmorel.gwtjackson.client.ObjectMapper;


public class CurrentSession {

    public static interface CurrentSessionMapper extends ObjectMapper<CurrentSession> {}

    private static final String sToken = "Token ";

    public String token;

    public User user;

    @JsonIgnore
    public static CurrentSession fromTokenString(String token) {
        CurrentSessionMapper mapper = GWT.create(CurrentSessionMapper.class);
        return mapper.read(token);
    }

    @JsonIgnore
    public String toTokenString() {
        CurrentSessionMapper mapper = GWT.create(CurrentSessionMapper.class);
        return mapper.write(this);
    }

    @JsonIgnore
    public String getServiceKey() {
        return sToken + token;
    }

    @JsonIgnore
    public String getUserName() {
        return user.username;
    }

    @JsonIgnore
    public void clear() {
        token = null;
        user = null;
    }
}
