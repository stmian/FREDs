var arDrone = require('ar-drone');
var client  = arDrone.createClient();

client.takeoff(function() {
	console.log("Took off");
});

client
	.after(5000, function() {
		this.clockwise(0.5);
	})
	.after(3000, function() {
		this.stop();
		this.land(function() {
			console.log("Landed.");
		});
	});

