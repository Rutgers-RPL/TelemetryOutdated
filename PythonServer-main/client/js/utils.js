function initDemoMap() {
  var Esri_WorldImagery = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    {
      attribution:
        "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, " +
        "AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
    }
  );

  var Esri_DarkGreyCanvas = L.tileLayer(
    "https://{s}.sm.mapstack.stamen.com/" +
      "(toner-lite,$fff[difference],$fff[@23],$fff[hsl-saturation@20])/" +
      "{z}/{x}/{y}.png",
    {
      attribution:
        "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, " +
        "NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community"
    }
  );

  var baseLayers = {
    Satellite: Esri_WorldImagery,
    "Grey Canvas": Esri_DarkGreyCanvas
  };

  var map = L.map("map", {
    layers: [Esri_WorldImagery]
  });

  var layerControl = L.control.layers(baseLayers);
  layerControl.addTo(map);
  map.setView([40.52, -78.39], 8);

  return {
    map: map,
    layerControl: layerControl
  };
}
var Color = function(hexOrObject) {
    var obj;
    if (hexOrObject instanceof Object) {
        obj = hexOrObject;
    } else {
        obj = LinearColorInterpolator.convertHexToRgb(hexOrObject);
    }
    this.r = obj.r;
    this.g = obj.g;
    this.b = obj.b;
}
Color.prototype.asRgbCss = function() {
    return "rgb("+this.r+", "+this.g+", "+this.b+")";
}

var LinearColorInterpolator = {
    // convert 6-digit hex to rgb components;
    // accepts with or without hash ("335577" or "#335577")
    convertHexToRgb: function(hex) {
        var match = hex.replace(/#/,'').match(/.{1,2}/g);
        return new Color({
            r: parseInt(match[0], 16),
            g: parseInt(match[1], 16),
            b: parseInt(match[2], 16)
        });
    },
    // left and right are colors that you're aiming to find
    // a color between. Percentage (0-100) indicates the ratio
    // of right to left. Higher percentage means more right,
    // lower means more left.
    findColorBetween: function(left, right, percentage) {
        var newColor = {};
        var components = ["r", "g", "b"];
        for (var i = 0; i < components.length; i++) {
            var c = components[i];
            newColor[c] = Math.round(left[c] + (right[c] - left[c]) * percentage / 100);
        }
        return new Color(newColor);
    }
}
//var csv is the CSV file with headers
function csvJSON(csv){
  var lines=csv.split("\n");

  var result = [];
  var headers=lines[0].split(",");
  for(var i=1;i<lines.length;i++){
      var obj = {};
      var currentline=lines[i].split(",");
      for(var j=0;j<headers.length;j++){
          obj[headers[j]] = currentline[j]-0;
      }
     result.push(obj);
  }
  return result; //JavaScript object
}
function ir(x){
  return x&&x!==-999;
}
function CSVJSON2GEOJSON(csvjson){
  window.csvjson = csvjson;
  var data = csvjson
  return {
    "name": "test flight path",
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": data.map(d=>{
            return [d.longitude,d.latitude,d.altitude]
          })
        },
        "properties": null
      }
    ]
  }
}
function createHookFn(Elevation,newdata){
  var dataName = newdata.name;
  Elevation.addInitHook(function () {
      var _this = this;

      var opts = this.options;
      var slope = {};
      slope.label = newdata.label;

      if (this.options.slope != "summary") {
        this._registerAxisScale({
          axis: "y",
          position: "right",
          tickPadding: 16,
          label: slope.label,
          labelX: 25,
          labelY: -8,
          name: dataName
        });

        this._registerAreaPath({
          name: dataName,
          label: dataName,
          yAttr: dataName,
          scaleX: 'distance',
          scaleY: dataName,
          color: '#F00',
          strokeColor: '#000',
          strokeOpacity: "0.5",
          fillOpacity: "0.25"
        });
      }

      this.on("eledata_updated", function (e) {
        var data = this._data;
        var i = e.index;
        var z = data[i].z;
        data[i][dataName] = window.flightData[i][dataName];
      });

      this._registerFocusLabel({
        name: dataName,
        chart: function chart(item) {
          return item[dataName].toFixed(2) + slope.label;
        },
        marker: function marker(item) {
          return Math.round(item[dataName]) + slope.label;
        }
      });

    });
  return;
}
// const STRUCT_FORMAT = '< I f f f f f f f f f d d I';
// const STRUCT_PROPS = ['magic','time','latitude','longitude','altitude','accx','accy','accz','mA','V','temp','pressure','checksum']
// const MAGIC = 0xBEEFF00D;
// function bufferToJSON(buffer){
//     var unpacked = struct.unpack(STRUCT_FORMAT, buffer);
//     var json = {};
//     for(var i=0;i<unpacked.length;i++){
//         json[STRUCT_PROPS[i]] = unpacked[i];
//     }
//     return json;
// }
// var SIZE = struct.sizeOf(STRUCT_FORMAT);