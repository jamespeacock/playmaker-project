package com.gwidgets.client;

import com.google.gwt.place.impl.AbstractPlaceHistoryMapper;
import com.gwidgets.client.MyHistoryMapper;
import com.google.gwt.place.shared.Place;
import com.google.gwt.place.shared.PlaceTokenizer;
import com.google.gwt.place.impl.AbstractPlaceHistoryMapper.PrefixAndToken;
import com.google.gwt.core.client.GWT;

public class MyHistoryMapperImpl extends AbstractPlaceHistoryMapper<Void> implements MyHistoryMapper {
  
  protected PrefixAndToken getPrefixAndToken(Place newPlace) {
    if (newPlace instanceof com.gwidgets.client.placesAndactivities.LoginPlace) {
      com.gwidgets.client.placesAndactivities.LoginPlace place = (com.gwidgets.client.placesAndactivities.LoginPlace) newPlace;
      PlaceTokenizer<com.gwidgets.client.placesAndactivities.LoginPlace> t = GWT.create(com.gwidgets.client.placesAndactivities.LoginPlace.Tokenizer.class);
      return new PrefixAndToken("LoginPlace", t.getToken((com.gwidgets.client.placesAndactivities.LoginPlace) place));
    }
    if (newPlace instanceof com.gwidgets.client.placesAndactivities.MainPagePlace) {
      com.gwidgets.client.placesAndactivities.MainPagePlace place = (com.gwidgets.client.placesAndactivities.MainPagePlace) newPlace;
      PlaceTokenizer<com.gwidgets.client.placesAndactivities.MainPagePlace> t = GWT.create(com.gwidgets.client.placesAndactivities.MainPagePlace.Tokenizer.class);
      return new PrefixAndToken("MainPagePlace", t.getToken((com.gwidgets.client.placesAndactivities.MainPagePlace) place));
    }
    return null;
  }
  
  protected PlaceTokenizer<?> getTokenizer(String prefix) {
    if ("MainPagePlace".equals(prefix)) {
      return GWT.create(com.gwidgets.client.placesAndactivities.MainPagePlace.Tokenizer.class);
    }
    if ("LoginPlace".equals(prefix)) {
      return GWT.create(com.gwidgets.client.placesAndactivities.LoginPlace.Tokenizer.class);
    }
    return null;
  }

}
