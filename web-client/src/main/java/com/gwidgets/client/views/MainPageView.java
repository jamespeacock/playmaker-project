package com.gwidgets.client.views;

import java.util.Arrays;
import java.util.List;

import com.google.gwt.place.shared.Place;
import com.google.gwt.user.cellview.client.CellTable;
import com.google.gwt.user.cellview.client.TextColumn;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;
import com.gwidgets.client.models.CurrentSession;

public class MainPageView extends Composite implements IsWidget {

	VerticalPanel container;
	HorizontalPanel leftPanel;
	private HorizontalPanel rightPanel;
	private HorizontalPanel formPanel;
	Button logout;
	List<String> data;
	private Presenter presenter;
	private CurrentSession session;
	CellTable<String> table;
	
	private final TextBox nameTextBox = new TextBox();

	private final TextBox taskTextBox = new TextBox();

	private final TextBox progressTextBox = new TextBox();

	private final TextBox scopeTextBox = new TextBox();

	Button button = new Button("Modify");

	
	public MainPageView(){
		leftPanel = new HorizontalPanel();
		rightPanel = new HorizontalPanel();
		formPanel = new HorizontalPanel();
		Label nameLabel = new Label("Username");

		Label taskLabel = new Label("Token");

		Label progressLabel = new Label("ID");

		Label scopeLabel = new Label("Scope");

		Button button = new Button("Modify");

		getFormPanel().add(nameLabel);
		getFormPanel().add(nameTextBox);
		getFormPanel().add(taskLabel);
		getFormPanel().add(taskTextBox);
		getFormPanel().add(progressLabel);
		getFormPanel().add(progressTextBox);
		getFormPanel().add(scopeLabel);
		getFormPanel().add(scopeTextBox);
		getFormPanel().add(button);

		table = new CellTable<String>();

		TextColumn<String> column1 = new TextColumn<String>(){
			@Override
			public String getValue(String object) {
				// TODO Auto-generated method stub
				return object.split(" ")[0];
			}

		};

		TextColumn<String> column2 = new TextColumn<String>(){
			@Override
			public String getValue(String object) {
				return object.split(" ")[1];
			}

		};

		TextColumn<String> column3 = new TextColumn<String>(){
			@Override
			public String getValue(String object) {
				return object.split(" ")[2];
			}

		};

		TextColumn<String> column4 = new TextColumn<String>() {
			@Override
			public String getValue(String object) {
				return object.split(" ")[3];
			}
		};

		table.addColumn(column1, "Username");
		table.addColumn(column2, "Token");
		table.addColumn(column3, "ID");
		table.addColumn(column4, "Scope");
	}

	public void init() {
		data = Arrays.asList(session.user.username + " " + session.token + " " + session.user.id + " " + session.user.scope);
		table.setRowData(data);
		getRightPanel().add(table);
		container = new VerticalPanel();
		logout = new Button("Logout");
		container.add(logout);
		container.add(leftPanel);
		container.add(getRightPanel());
	}

	@Override
	public Widget asWidget() {
		return container;
	}

	public void setPresenter(Presenter presenter) {
		this.presenter = presenter;
	}

	public void setSession(CurrentSession session) {this.session = session; }

	public HorizontalPanel getFormPanel() {
		return formPanel;
	}


	public HorizontalPanel getRightPanel() {
		return rightPanel;
	}


	public interface Presenter{
		 void goTo(Place place);
	}
}
