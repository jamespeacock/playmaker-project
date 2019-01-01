package com.gwidgets.client.placesAndactivities;

import com.google.gwt.activity.shared.AbstractActivity;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.shared.EventBus;
import com.google.gwt.place.shared.Place;
import com.google.gwt.user.client.ui.AcceptsOneWidget;
import com.gwidgets.client.ClientFactory;
import com.gwidgets.client.views.LoginView;

public class LoginActivity extends AbstractActivity implements LoginView.Presenter {
	
	ClientFactory factory;
	
	String name;
	
	public LoginActivity(LoginPlace loginPlace, ClientFactory clientFactory){
		this.factory = clientFactory;
		this.name = loginPlace.getLoginName();
	}

	@Override
	public void start(AcceptsOneWidget panel, EventBus eventBus) {
		// TODO Auto-generated method stub
		LoginView view = factory.getLoginView();
        view.setPresenter(this);
		panel.setWidget(view.asWidget());
		
	}

	/**
	 * Ask user before stopping this activity
	 */
	@Override
	public String mayStop() {
		return "You are being redirected to Spotify Login Page";
	}
	
	@Override
	public void goTo(Place place) {
		factory.getPlaceController().goTo(place);
	}
}
