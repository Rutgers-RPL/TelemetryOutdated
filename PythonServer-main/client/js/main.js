var url = (document.location.href.startsWith('https')?'wss://':'ws://')+document.domain
console.log('WEBSOCKET CONNECTIN TO: ',url)
var socket = new WebSocket(url);
var mapStuff = initDemoMap();
var map = mapStuff.map;
var layerControl = mapStuff.layerControl;
var ui = new UI(map);
var NEEDSINIT = true;

var initialTime = -999
var frameSize = 1000 //maximum number of datapoints
var n = 0
var data = {}
data.temp = {points:[],chart:0};
data.temp.chart = new CanvasJS.Chart("tempChart", {
	title:{
		text: "Temperature"
	},
	data: [{
			 type: "line",
			 dataPoints: data.temp.points
		}]
});

data.pressure = {points:[],chart:0};
data.pressure.chart = new CanvasJS.Chart("pressureChart", {
	title:{
		text: "Pressure"
	},
	data: [{
			 type: "line",
			 dataPoints: data.pressure.points
		}]
});

data.altitude = {points:[],chart:0};
data.altitude.chart = new CanvasJS.Chart("altitudeChart", {
	title:{
		text: "Altitude"
	},
	data: [{
			 type: "line",
			 dataPoints: data.altitude.points
		}]
});

data.accx = {points:[],chart:0};
data.accx.chart = new CanvasJS.Chart("accxChart", {
	title:{
		text: "Acceleration x"
	},
	data: [{
			 type: "line",
			 dataPoints: data.accx.points
		}]
});

  // Set event handlers.
socket.onopen = function() {
    console.log("onopen");
    for(var i in data)
    	data[i].chart.render();
};

async function main(){
    // var data = await fetch('data/test.csv').then(resp=>resp.text())
    // //console.log(data);
    // var json = csvJSON(data);
    //console.log(json);
    
    socket.addEventListener('open', function (event) {
        console.log('CONNECTED TO WEBSOCKET')
    });
    socket.addEventListener('message', function (event) {
        const message= JSON.parse(event.data);
        ui.addData(message);
        ui.render();
        console.log('< DATA RECIEVED >')
        if(NEEDSINIT){
            map.fitBounds(ui.polyline.getBounds());
        }
        
		n+=1;
		console.log(n);
		if(initialTime == -999)
			initialTime = message.time;
		data.temp.points.push({x:message.time,y:message.temp})
		data.pressure.points.push({x:message.time,y:message.pressure})
		data.altitude.points.push({x:message.time,y:message.altitude})
		data.accx.points.push({x:message.time,y:message.accx})
		for(var i in data){
			if(data[i].points.length > frameSize)
				data[i].points.shift();
			data[i].chart.render();
		}
    });
    // ui.setData(json);
    // ui.render();
    // map.fitBounds(ui.polyline.getBounds());
}
main();