var arDrone = require('ar-drone');
var client = arDrone.createClient();
//client.takeoff();



  process.stdin.resume();
  process.stdin.setEncoding('utf8');
  var util = require('util');

  process.stdin.on('data', function (text) {
    console.log('received data:', util.inspect(text));
    if (text === 'quit\r\n') {
      done(); }
    if(text === 'w\r\n')
	{
		client.front();
	}
	if(text === 's\r\n')
	{
		client.back();
	
	}
  });

  function done() {
    console.log('Now that process.stdin is paused, there is nothing more to do.');
    process.exit();
  }

  
  

//client.takeoff();

/*client
  .after(5000, function() {
    this.clockwise(0.5);
  })
  .after(3000, function() {
    this.animate('flipLeft', 15);
  })
  .after(1000, function() {
    this.stop();
    this.land();
  });
  
  */