React architecture

# Top level layout
<store>
	<App.ContextProvider>
		<Routes>
		 	<Dashboard 
		 		user={this.props.user}
	 		/>
		 	<Controller
				user={this.props.user}
				controller={this.props.controller}
			/>
            <Listener
				user={this.props.user}
				listener={this.props.listener}
              />
			<Login 
				user={this.props.user}
			/>
			<Signup 
				user={this.props.user}
			/>
      </Routes>	
	</App.ContextProvider>	
</store>

# See each Route's class (ex: components/Dashboard/Dashboard.js)
# I think I have too much logic in each class as well as the rendered format


#All components have Header at top except Dashboard
TODO Want Header to be above router

#List of reusable compoents
 SongTable (display search result songs & songs in queue)
 Devices (modal for device list and selection)
 Search (searchbar)

# Don't have separation between presentational and functional components. Not exactly sure how to accomplish this.


#### REDUX ####

One reducers.js contains objects:
  - user
  - controller
  - listener 

One actions.js contains actions:
  - checkLoggedIn, --> user
  - setDevice, --> user.current_device
  - refreshDevices, --> user.devices
  - startController, --> controller
  - startListener, --> listener


#Some components get items as props but Ideally I think I'd want everything to be grabbed from Context. Is that right?


#### API CLIENT ####
All api call handlers live in playmaker/api. There are 4
 - ApiInterface.js (root class, others inherit from it. Calls "GET" & "POST", accepts a url and request body)
 - ControllerInterface.js (has specific controller api calls as methods)
 - ListenerInterface.js (has specific listener api calls as methods)
 - SongsInterface.js (has specific song search api calls as methods)



#WHAT CAN IMPROVE
since I changed how/when/where I call the api and change state many times, the app does this in 2-3 different ways. I want to pick one and stick with it.
It is my understanding you want all api calls to live in actions.js and all state changes to live in reducers.js. I am in the process of getting that standard everywhere

What is lacking is how state is then passed into presentational components. Especially if a button on that presentation component needs to kickoff an action.

2nd big thing. Each page/route/component checks if the user is logged in before rendering. what's the cleanest way to check something from the api before rendering. I hate that it renders with the default isLoggedIn=False, then makes the call, then refreshes if it turns out isLoggedIn is true!!!

Let me know if you have any questions!



