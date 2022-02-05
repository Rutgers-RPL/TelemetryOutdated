const struct = require('python-struct');
const fs = require("fs")
const STRUCT_FORMAT = '< I f f f f f f f f f d d I';
const STRUCT_PROPS = ['magic','time','latitude','longitude','altitude','accx','accy','accz','mA','V','temp','pressure','checksum']
const MAGIC = 0xBEEFF00D;
function bufferToJSON(buffer){
    var unpacked = struct.unpack(STRUCT_FORMAT, buffer);
    var json = {};
    for(var i=0;i<unpacked.length;i++){
        json[STRUCT_PROPS[i]] = unpacked[i];
    }
    return json;
}

var size = struct.sizeOf(STRUCT_FORMAT); // --> 29

var start = size-1;
var fileData = Buffer.from(fs.readFileSync('gpsdump.bin'), 'binary');

var foundstart = false;
while(!foundstart){
    console.log(start)
    var testbuffer = fileData.slice(start,start+size);
    var unpacked = bufferToJSON(testbuffer)
    console.log(unpacked)
    foundstart = (unpacked.magic==MAGIC)||start>size;
    if(!foundstart){
        start ++;
    }
}
console.log('start was at ',start)



//struct.unpack('>iixxQ10sb', Buffer.from('000004d20000162e0000ab54a98ceb1f0ad26162636465666700000001', 'hex')); // --> [ 1234, 5678, 12345678901234567890, 'abcdefg', 1 ]
