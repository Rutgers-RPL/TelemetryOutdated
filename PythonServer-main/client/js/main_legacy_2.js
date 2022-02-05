var controlElevation,controlLayer,map;
var flightData = [];
var decoder = new TextDecoder();
var totaltext = '';
async function main(){
    loadCsv(10);
}
async function loadCsv(to){
    var data = await fetch('data/test.csv').then(resp=>resp.text())
    var json = csvJSON(data);
    json = json.filter(d=>{
        for(var i in d){
            if(!ir(d[i]))
                return false;
        }
        return true;
    });
    //console.log(json[0],json.length)
    window.flightData = json;
    var geojson = CSVJSON2GEOJSON(json);
    loadData(geojson)
    // window.upOne = function(){
    //     to+=20;
    //     var geojson = CSVJSON2GEOJSON(json.slice(0,to));
    //     addData(geojson)
    // }
}
window.loadCsv = loadCsv;
async function loadData(geojson){
    // createHookFn(L.Elevation,{
    //     name:'accy',
    //     label:'m/s^2'
    // })
    // createHookFn(L.Elevation,{
    //     name:'accx',
    //     label:'m/s^2'
    // })
    // createHookFn(L.Elevation,{
    //     name:'accz',
    //     label:'m/s^2'
    // })
    var opts = {
    	map: {
    		center: [41.4583, 12.7059],
    		zoom: 5,
    		fullscreenControl: false,
    		resizerControl: true,
    		preferCanvas: true,
    		rotate: true,
    		rotateControl: {
    			closeOnZeroBearing: true
    		},
    	},
    	elevationControl: {
    	    data:JSON.stringify(geojson),
    		//url: "https://raruto.github.io/leaflet-elevation/examples/demo.geojson",
    		options: {
    			theme: "lime-theme",
    			collapsed: false,
    			autohide: false,
    			autofitBounds: true,
    			position: "bottomleft",
    			detached: true,
    			summary: "multiline",
    			imperial: false,
    			slope: false,
    			speed: false,
    			acceleration: false,
    			//time: true,
    			legend: true,
    			followMarker: true,
    			almostOver: true,
    			distanceMarkers: false,
    			distance: false,
    		},
    	},
    	layersControl: {
    		options: {
    			collapsed: false,
    		},
    	},
    };
    if(!map){
        map = L.map('map', opts.map);
    }
    // if(controlElevation){
    //     map.removeLayer(controlElevation);
    //     if (map.hasLayer(controlLayer)) map.removeLayer(controlLayer);
    // }
    controlElevation = L.control.elevation(opts.elevationControl.options);
    controlLayer = L.control.layers(null, null, opts.layersControl.options);
    
    controlElevation.addTo(map);
    //controlLayer.addTo(map);
    
    // controlElevation.on('eledata_loaded', function(e) {
    // 	controlLayer.addOverlay(e.layer, e.name);
    // });
    console.log('elevation control')
    window.ree = opts.elevationControl.data;
    
    
    controlElevation.load(geojson);
    
}
function addData(data){
    controlElevation.clear();
    for(var i in map._layers){
        var l = map._layers[i];
        if(l._latlngs){
            map.removeLayer(l)
        }
    }
    //map.removeControl(controlElevation);
    // map.removeLayer(controlLayer);
    // map.removeLayer(controlElevation)
    // controlElevation.clear();
    // console.log(data);
    controlElevation.load(data)
}

main();