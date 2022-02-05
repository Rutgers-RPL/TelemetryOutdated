// var map = new L.Map('map', { mapTypeId: 'terrain', center: [41.4583, 12.7059], zoom: 5 });

// // Instantiate elevation control.
// var controlElevation = L.control.elevation(elevation_options).addTo(map);

// // Load track from url (allowed data types: "*.geojson", "*.gpx", "*.tcx")
// controlElevation.load("https://raruto.github.io/leaflet-elevation/examples/via-emilia.gpx");

var mapStuff = initDemoMap();
var map = mapStuff.map;
var layerControl = mapStuff.layerControl;
var ui = new UI(map);
async function main(){
    var data = await fetch('data/test.csv').then(resp=>resp.text())
    //console.log(data);
    var json = csvJSON(data);
    //console.log(json);
    ui.setData(json);
    ui.render();
    map.fitBounds(ui.polyline.getBounds());
}
main();