package com.gwidgets.client.models;

import com.fasterxml.jackson.annotation.JsonIgnore;

import java.util.List;
import java.util.Objects;

public class User {

    public Integer id;

    public String username;

//    public Boolean is_superuser;

    public String access_token;

    public String scope;

    @JsonIgnore
    public static User getUserById(Integer id, List<User> userList) {
        return userList.stream()
                .filter(user -> Objects.equals(user.id, id))
                .findFirst()
                .orElse(null);
    }
}
