const express = require('express');
const app = express();
const expressWs = require('express-ws')(app);
const struct = require('python-struct');
const fs = require("fs")
const STRUCT_FORMAT = '< I f f f f f f f f f d d I';
const STRUCT_PROPS = ['magic','time','latitude','longitude','altitude','accx','accy','accz','mA','V','temp','pressure','checksum']
const MAGIC = 0xBEEFF00D;
const size = struct.sizeOf(STRUCT_FORMAT);
const JUMP = 56; // JUMP this much to get to next struct in data
function bufferToJSON(buffer){
    var unpacked = struct.unpack(STRUCT_FORMAT, buffer);
    var json = {};
    for(var i=0;i<unpacked.length;i++){
        json[STRUCT_PROPS[i]] = unpacked[i];
    }
    return json;
}
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

var args = require('minimist')(process.argv.slice(2));

const TESTING = args.mode&&args.mode=='testing';
const DATASOURCE = args.data||'./data/gpsdump.bin' // can be either 'bin' (binary serial dump), 'csv' (csv data dump), or 'serial' (read from serial)
const START = args.start-0||0;
const sockets = [];

if(TESTING){
    var start = START;
    var testData = [];
    if(DATASOURCE.endsWith('bin')){
        var fileData = Buffer.from(fs.readFileSync(DATASOURCE), 'binary');
        const bufferLen = fileData.toString().length;
        for(var i=0;i<bufferLen;i+=JUMP){
            var testbuffer = fileData.slice(i,i+size);
            testData.push(bufferToJSON(testbuffer));
        }
    }else if(DATASOURCE.endsWith('csv')){
        testData = csvJSON(fs.readFileSync(DATASOURCE).toString());
    }
    
    setInterval(function(){
        if(sockets.length>0||true){
            var unpacked = testData[start]
            if(unpacked.magic==MAGIC){
                for(var i=0;i<sockets.length;i++){
                    sockets[i].send(JSON.stringify(unpacked))
                }
            }else{
                console.warn('MAGIC NOT MATCHING ')
            }
            
            start++;
        }
    },100);
}

app.get('/', function(req, res, next){
  console.log('get route', );
  res.end();
});

app.ws('/', function(ws, req) {
    sockets.push(ws);
    ws.on('close',function(){
        sockets.splice(sockets.indexOf(ws),1);
    })
    console.log('<- CLIENT CONNECTED ->')
});


app.listen(8080);
console.log('server started')