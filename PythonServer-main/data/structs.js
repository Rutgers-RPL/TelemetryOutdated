const fs = require("fs")
var fileData = Buffer.from(fs.readFileSync('gpsdump.bin'), 'binary');
// var _ = require('c-struct');
// var inputParam = new _.Schema({
//   inputFlag: _.type.uint16,  // ushort
//   inputName: _.type.string() // string is 0-terminated
// });
// // register to cache
// _.register('InputParam', inputParam);

// var out = [];
// for (var i = 0; i < fileData.length; i+=60) {
//   var partial = fileData.slice(i, i+60);
//   out.push(_.unpackSync('InputParam', partial));
// }
// console.log(out);
var _ = require('c-struct');
/*

DARRELData = namedtuple('DARRELData', [
'magic',
'time',
'latitude',
'longitude',
'altitude',
'accx',
'accy',
'accz',
'mA',
'V',
'temp',
'pressure',
'checksum'
])
DARRELData_raw = struct.Struct('< I f f f f f f f f f d d I') # 1 int 9 floats 2 doubles
*/
var playerSchema = new _.Schema({
    'magic':_.type.uint16,
    'time',
    'latitude',
    'longitude',
    'altitude',
    'accx',
    'accy',
    'accz',
    'mA',
    'V',
    'temp',
    'pressure',
    'checksum',
  id: _.type.uint16,
  name: _.type.string(16),
  hp: _.type.uint24,
  exp: _.type.uint32,
  status: _.type.uint8,
  motd: _.type.string(), // null-terminated if no length
  motw: _.type.string(), // cstring if no length
  skills: [{
    id: _.type.uint8,
    name: _.type.string(32),
    secret: _.type.uint40
  }],
  position: {
    x: _.type.uint16,
    y: _.type.uint16
  },
  hash: _.type.uint48
});

// register to cache
_.register('Data', playerSchema);

// buffer to object | this can be on another file
var obj = _.unpackSync('Player', fileData);