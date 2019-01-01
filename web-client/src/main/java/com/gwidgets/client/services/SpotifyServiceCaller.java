package com.gwidgets.client.services;

import com.gwidgets.client.models.Playlist;
import com.gwidgets.client.models.User;
import org.fusesource.restygwt.client.MethodCallback;
import org.fusesource.restygwt.client.RestService;

import java.util.List;
import javax.ws.rs.*;

public interface SpotifyServiceCaller extends RestService {

    @GET
    @Path("http://localhost:8000/login")
    void login(@PathParam("path") String path,
               @QueryParam("username") String username,
               MethodCallback<User> authenticateCallback);

    @GET
    @Path("{path}/playlists")
    void fetchPlaylists(@HeaderParam("Authorization") String token,
                        @PathParam("path") String path,
                        MethodCallback<List<Playlist>> fetchInitialPlaylistCallback);
}
