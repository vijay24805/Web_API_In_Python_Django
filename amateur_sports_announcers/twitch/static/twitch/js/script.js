$(document).ready(function() {

	//using official TwitchTV Example Formatting: http://justintv.github.io/twitch-js-sdk/example.html
	window.CLIENT_ID = 'jqsd54ktgrxu0x05kh6w2lt4l3zkfck';
	$(function() {
		// Initialize. If we are already logged in, there is no
		// need for the connect button
		Twitch.init({clientId: CLIENT_ID}, function(error, status) {
			if (error) {
				// error encountered while loading
				console.log(error);
			}
			if (status.authenticated) {
				// we are now logged in
				// show the data for logged-in users
				Twitch.api({method: 'user'}, function(error, user) {
					$('#welcomeBanner').append("Welcome " + user.display_name + ",");
				});
				$('.authenticate').hide();
				$('.authenticated').show();
			}
			/* removing this else condition
			  as it is not required
			*/
			/*
			else {
				// Show the twitch connect button
				$('.authenticate').show();
				$('.authenticated').hide();
			}
			*/
		});
		$(".twitch-connect").click(function() {
			Twitch.login({
				scope: ['user_read', 'channel_read']
			});
		});
		$('#logout').click(function() {
			Twitch.logout();

			// Reload page and reset url hash. You shouldn't
			// need to do this.
			window.location = window.location.pathname
		});

	});

});









  
