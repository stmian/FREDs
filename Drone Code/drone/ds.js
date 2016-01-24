var express = require('express');
var app = express();

var turnSpeed = .2;
var moveSpeed = .2;
var vertSpeed = .2;

var arDrone = require('ar-drone');
var drones = [
	arDrone.createClient({ip: '192.168.1.200'}),
	arDrone.createClient({ip: '192.168.1.202'})
];

app.get('/takeoff', function(req, res) {
	gc('Taking off.', res)
	drones.forEach(function(drone){
		drone.takeoff();
	});

	diff(drones[1]);
});

app.get('/tr', function(req, res) {
	gc('Turning right', res)
	drones.forEach(function(drone){
		drone.clockwise(turnSpeed);
	});
});
app.get('/tl', function(req, res) {
	gc('Turning left', res)
	drones.forEach(function(drone){
		drone.counterClockwise(turnSpeed);
	});
});
app.get('/mr', function(req, res) {
	gc('Moving right', res)
	drones.forEach(function(drone){
		drone.right(moveSpeed);
	});
});
app.get('/ml', function(req, res) {
	gc('Moving left', res)
	drones.forEach(function(drone){
		drone.left(moveSpeed);
	});
});
app.get('/u', function(req, res) {
	gc('Moving up', res)
	drones.forEach(function(drone){
		drone.up(vertSpeed);

	});
});
app.get('/d', function(req, res) {
	gc('Moving down', res)
	drones.forEach(function(drone){
		drone.down(vertSpeed);

	});
});
app.get('/f', function(req, res) {
	gc('Moving forward', res)
	drones.forEach(function(drone){
		drone.front(moveSpeed);
	});
});
app.get('/b', function(req, res) {
	gc('Moving backward', res)
	drones.forEach(function(drone){
		drone.back(moveSpeed);
	});
});

app.get('/panic', function(req, res) {
	gc('Panicking!', res)
	drones.forEach(function(drone){
		drone.land();
	});
});

app.get('/land', function(req, res) {
	gc('Landing', res);
	drones.forEach(function(drone){
		drone.stop();
	});
	drones.forEach(function(drone){
		drone.land();
	});
});

// default case
app.get('*', function(req, res) {
	gc('Received unknown command. Halting.', res)
	drones.forEach(function(drone){
		drone.stop();
	});
});

function gc(out, response) {
	console.log(out);
	response.sendStatus(200);
}

function diff(drone) {
	drone.up(vertSpeed);
	drone.after(10000,function(){
		this.stop();
	});
}

app.listen(3000);
