var UI = function(map){
  var obj = this;
  obj.map = map;
  var style = {color:'red',weight:3}
  var hoverStyle = {color:'blue',weight:7}
  obj.polyline =L.polyline([], style).addTo(map);
  obj.latlngs = []
  obj.polyline.on('mouseover', function(e) {
      var closest = L.GeometryUtil.closest(map, obj.latlngs, [e.latlng.lat, e.latlng.lng])
      console.log(closest)
      // console.log(obj.polyline)
      // console.log(e)
      var layer = e.target;
      layer.setStyle(hoverStyle);
  });
  obj.polyline.on('mouseout', function() {
    this.setStyle(style)
  });
  obj.data = [];
  obj.setData = function(data){
    obj.data = data;
  }
  obj.addData = function(newdata){
    obj.data.push(newdata)
  }
  obj.renderPath = function(){
    var latlngs = obj.data.map(function(d){
      return [d.latitude,d.longitude];
    })
    latlngs = obj.latlngs =  latlngs.filter(d=>d[0]&&d[1]&&d[0]!==-999&&d[1]!==-999)
    obj.polyline.setLatLngs(latlngs);
    // var latlngs = [
    //     [45.51, -122.68],
    //     [37.77, -122.43],
    //     [34.04, -118.2]
    // ];
    
    // var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
  }
  obj.render = function(){
    obj.renderPath();
  }
  return this;
}