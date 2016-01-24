function panic(client, callback) {
	client.stop();
	client.land(function() {
		callback();
	});	
}
