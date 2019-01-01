package com.gwidgets.client.services;

import com.google.gwt.core.client.GWT;
import com.gwidgets.client.models.Playlist;
import com.gwidgets.client.models.User;
import org.fusesource.restygwt.client.MethodCallback;
import com.gwidgets.client.common.UrlHelper;

import java.util.List;

public class SpotifyService {

    SpotifyServiceCaller service = GWT.create(SpotifyServiceCaller.class);

    public void login(String username, MethodCallback<User> authenticateCallback) {
        GWT.log(UrlHelper.sDEFAULT_BACKEND_URL + " - " + username);
        service.login(UrlHelper.sDEFAULT_BACKEND_URL, username, authenticateCallback);
    }

    public void fetchPlaylists(String token, String path, MethodCallback<List<Playlist>> fetchInitialPlaylistCallback) {

    }
}
