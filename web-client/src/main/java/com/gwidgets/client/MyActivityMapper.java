package com.gwidgets.client;

import com.google.gwt.activity.shared.Activity;
import com.google.gwt.activity.shared.ActivityMapper;
import com.google.gwt.place.shared.Place;
import com.gwidgets.client.common.UrlHelper;
import com.gwidgets.client.placesAndactivities.LoginActivity;
import com.gwidgets.client.placesAndactivities.LoginPlace;
import com.gwidgets.client.placesAndactivities.MainPageActivity;
import com.gwidgets.client.placesAndactivities.MainPagePlace;

public class MyActivityMapper implements ActivityMapper {
	private ClientFactory clientFactory;
	
	public MyActivityMapper(ClientFactory factory){
		super();
		this.clientFactory = factory;
		UrlHelper.configureConnectionURLs();
	}
	@Override
	public Activity getActivity(Place place) {
		if(place instanceof LoginPlace){
			return new LoginActivity((LoginPlace) place, clientFactory);
		}else if(place instanceof MainPagePlace) {
			return new MainPageActivity((MainPagePlace) place, clientFactory);
		}
		   return null;
	}

	//TODO for deployment, create ConnectionHelper
//	import com.google.gwt.user.client.Window;
//	import org.fusesource.restygwt.client.Defaults;
//	public class ConnectionHelper {
//		public String gatherHostInformation() { return Window.Location.getHost();}
//		public void setDefaultServiceRoot(String url) { Defaults.setServiceRoot(url);}
//	}

}
