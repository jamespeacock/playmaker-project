package com.gwidgets.client.placesAndactivities;

import com.google.gwt.activity.shared.AbstractActivity;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.shared.EventBus;
import com.google.gwt.place.shared.Place;
import com.google.gwt.user.client.ui.AcceptsOneWidget;
import com.google.gwt.view.client.CellPreviewEvent;
import com.google.gwt.view.client.CellPreviewEvent.Handler;
import com.gwidgets.client.ClientFactory;
import com.gwidgets.client.models.CurrentSession;
import com.gwidgets.client.views.MainPageView;

import javax.swing.plaf.ColorUIResource;

public class MainPageActivity extends AbstractActivity implements MainPageView.Presenter {
	
	ClientFactory factory;
	
	String name;
	
	MainPageView view;

	CurrentSession session;
	
	public MainPageActivity(MainPagePlace mainPagePlace, ClientFactory clientFactory){
		this.factory = clientFactory;
		this.name = mainPagePlace.getPlaceName();
		this.session = mainPagePlace.getSession();
		view = clientFactory.getMainPageView();
	}

	@Override
	public void start(AcceptsOneWidget panel, EventBus eventBus) {
		MainPageView view = factory.getMainPageView();
		view.setSession(session);
        view.setPresenter(this);
        view.init();
		panel.setWidget(view.asWidget());
	}
	
	@Override
	public void goTo(Place place) {
		factory.getPlaceController().goTo(place);
		
	}

}
