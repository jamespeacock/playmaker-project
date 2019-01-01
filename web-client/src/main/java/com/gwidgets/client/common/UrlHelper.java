package com.gwidgets.client.common;

import com.google.gwt.user.client.Window;

public class UrlHelper {

    public static String sPROTOCOL;

    public static String sDEFAULT_BACKEND_URL;

    public static void configureConnectionURLs() {
//        String hostInformation = Window.Location.getHost();
//        String host = hostInformation.replace("8080", "");
//        sPROTOCOL = "https";
//        if (hostInformation.contains("localhost") ||
//                hostInformation.contains("127.0.0.1")) {
//            host = host.replace("8888", "8000");
//            sPROTOCOL = "http";
//        }
//        sDEFAULT_BACKEND_URL = sPROTOCOL + "://" + host;
        sDEFAULT_BACKEND_URL = "http://localhost:8000/";
    }
}
