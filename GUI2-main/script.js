let input = document.querySelector('input');
//let textarea = document.querySelector('textarea');
let lines = [];
let line = -10;
let data = [];

function updateData() {
  line += 10;
  var string = lines[line].split(" ");
  data = string;
}

function getX() {
  return data[5];
}
function getY() {
  return data[6];
}
function getZ() {
  return data[7];
}
function getAlt() {
  return data[4];
}
function getTemp() {
  return data[10];
}
function getPressure() {
  return data[11];
}


input.addEventListener('change', () => {
    let files = input.files;
    if(files.length == 0) return;
    const file = files[0];
    let reader = new FileReader();
    reader.onload = (e) => {
        const file = e.target.result;
        lines = file.split(/\r\n|\n/);

        updateData();
        Plotly.newPlot('temp',[{
          y:[getTemp()],
          type:'line',
          name:'Temperature',
          line: {
            color: 'rgb(100, 100, 250)',
            width:1
          }
        }], {
              title:'Temperature',
              height:350
        }, {
            responsive:true,
            showlegend:false
        });
        Plotly.newPlot('pressure',[{
          y:[getPressure()],
          type:'line',
          name:'Pressure',
          line: {
            color: 'rgb(250, 100, 100)',
            width:1
          }
        }], {
              title:'Pressure',
              height:350
        }, {
            responsive:true,
            showlegend:false
        });
        Plotly.newPlot('alt',[{
          y:[0],
          type:'line',
          name:'Altitude',
          line: {
            color: 'rgb(250, 150, 50)',
            width:1
          }
        }], {
              title:'Altitude',
              height:350
        }, {
            responsive:true,
            showlegend:false
        });
        Plotly.newPlot('all',[{
               y:[getX()],
               type:'line',
               name:'X',
               line: {
                 color: 'rgb(255, 0, 0)',
                 width:1
               }
        }, {
              y:[getY()],
              type:'line',
              name:'Y',
              line: {
                color: 'rgb(0, 255, 0)',
                width:1
              }
        }, {
              y:[getZ()],
              type:'line',
              name:'Z',
              line: {
                color: 'rgb(0, 0, 255)',
                width:1
              }
        }], {
              title:'Acceleration',
              height:350
        },  {
              responsive:true,
              showlegend:false
        });

        setInterval(function() {
           updateData();
           Plotly.extendTraces('temp', { y: [[getTemp()]]}, [0]);
           Plotly.extendTraces('pressure', { y: [[getPressure()]]}, [0]);
           if (getAlt() != "-999.0") {
             Plotly.extendTraces('alt', { y: [[getAlt()]]}, [0]);
           } else {
             Plotly.extendTraces('alt', { y: [[0]]}, [0]);
           }
           Plotly.extendTraces('all', { y: [[getX()],[getY()],[getZ()]]}, [0, 1, 2]);
        }, 20);
    };
    reader.onerror = (e) => alert(e.target.error.name);
    reader.readAsText(file);

});
