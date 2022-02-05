const fs = require("fs")
var fileData = Buffer.from(fs.readFileSync('gpsdump.bin'), 'binary');
let struct = require("./structjs") // Node specific, you need to wrap it.
console.log(struct)
let someStruct = struct.struct('< I f f f f f f f f f d d I'); // This is your struct definition
console.log(fileData)
// let ws = new WebSocket("ws://URI");
// ws.binaryType = "arraybuffer";

// ws.onmessage = e => {
//     // Unpack using the structure definition. Unpack takes an ArrayBuffer.
//     let [id, username, amountDue] = someStruct.unpack(e.data);
//     // Use data...
// };