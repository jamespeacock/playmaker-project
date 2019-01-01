package com.gwidgets.client.placesAndactivities;

import com.google.gwt.place.shared.Place;
import com.google.gwt.place.shared.PlaceTokenizer;
import com.gwidgets.client.models.CurrentSession;

public class MainPagePlace extends Place {

	private CurrentSession session;

	public MainPagePlace(CurrentSession session) {
		this.session = session;
	}

	public String getPlaceName() {
		return "main app page";
	}

	public CurrentSession getSession() { return session; }

	public static class Tokenizer implements PlaceTokenizer<MainPagePlace> {
		@Override
		public String getToken(MainPagePlace place) {
			return place.session.toTokenString();
		}

		@Override
		public MainPagePlace getPlace(String token) {
			return new MainPagePlace(createFromString(token));
		}
	}

	public static CurrentSession createFromString(String token) {

		return CurrentSession.fromTokenString(token);
	}
}
