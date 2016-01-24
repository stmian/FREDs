var Myo = require('myo');
var myMyo = Myo.create();
var http = require('http');

myMyo.on('connected', function () {
        myo.setLockingPolicy('none');
});


myMyo.on('fist', function(edge){
    if(!edge) return;
    //fly up
    else {
        http.get("http://192.168.1.201:3000/u", function(res){});
        console.log("going up");
    }
});

myMyo.on('rest', function(edge) {
    if(!edge) return;
    //drones hover
    else {
        http.get("http://192.168.1.201:3000/stop", function(res){});
        console.log("hovering");
    }
});

myMyo.on('wave_in', function(edge) {
    if(!edge) return;
    //fly down
    else {
        http.get("http://192.168.1.201:3000/d", function(res){ });
        console.log("going down");
    }
});
