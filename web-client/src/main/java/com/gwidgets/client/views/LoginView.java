package com.gwidgets.client.views;

import com.google.gwt.core.client.GWT;
import com.google.gwt.place.shared.Place;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.*;
import com.gwidgets.client.models.CurrentSession;
import com.gwidgets.client.models.User;
import com.gwidgets.client.placesAndactivities.MainPagePlace;
import com.gwidgets.client.services.SpotifyService;
import org.fusesource.restygwt.client.Method;
import org.fusesource.restygwt.client.MethodCallback;


public class LoginView extends Composite implements IsWidget {

	private static LoginViewUiBinder uiBinder = GWT.create(LoginViewUiBinder.class);

	@UiField
	TextBox usernameField;
	@UiField
	Button loginButton;
	private Presenter presenter;
	private SpotifyService service;

	public LoginView() {
		initWidget(uiBinder.createAndBindUi(this));
		service = GWT.create(SpotifyService.class);
		loginButton.addClickHandler(event -> service.login(usernameField.getText(), authenticateCallback()));
	}

	private MethodCallback<User> authenticateCallback() {
		return new MethodCallback<User>() {
			@Override
			public void onFailure(Method method, Throwable exception) {
				GWT.log("Failure on authentication");
				GWT.log("Message: " + exception.getMessage());
			}

			@Override
			public void onSuccess(Method method, User response) {
				CurrentSession session = new CurrentSession();
				session.user = response;
				session.token = response.access_token;
				presenter.goTo(new MainPagePlace(session));
			}
		};
	}

	interface LoginViewUiBinder extends UiBinder<Widget, LoginView> {
	}
	
	public Presenter getPresenter() {
		return presenter;
	}

	public void setPresenter(Presenter presenter) {
		this.presenter = presenter;
	}

	public interface Presenter{
		void goTo(Place place);
	}

}
