
//reference associated example sketches for in depth comments regarding proper implementation

//TODO:
/*
// 1 test that accelerometer still works
// 2 test if gps code is necessary
// 3 try to lower the main frequency
*/

#include <Wire.h>

#include <Adafruit_GPS.h>
Adafruit_GPS GPS(&Serial2);

#include <MS5xxx.h>
MS5xxx sensor(&Wire);

#include <Adafruit_INA219.h>
Adafruit_INA219 ina219;

#include <Adafruit_H3LIS331.h>
#include <Adafruit_Sensor.h>

Adafruit_H3LIS331 lis = Adafruit_H3LIS331();
sensors_event_t event;

typedef struct __attribute__((packed)) data{
   int magic = 0xBEEFF00D;
   float time;
   float latitude; //assuming north of equator and west of prime meridian
   float longitude; //char lat and char lon for east/west and north/south
   float altitude;
   float accx;
   float accy;
   float accz;
   float mA;
   float V;
   double temp;
   double pressure;
} data;

void setup()
{
  Serial.begin(115200);

  //gps
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);   // 10 Hz update rate of gps
  GPS.sendCommand(PGCMD_ANTENNA);

  //ms5
  while (sensor.connect() > 0) {
    Serial.println("ms5 Error connecting...");
  }

  //ina
  uint32_t currentFrequency;
  while (!ina219.begin()) Serial.println("Failed to find INA219 chip");

  //h3lis331
  if (! lis.begin_I2C()) {   // change this to 0x19 for alternative i2c address
    Serial.println("Couldnt start");
  }

  lis.setRange(H3LIS331_RANGE_100_G);   // 6, 12, or 24 G
  lis.setDataRate(LIS331_DATARATE_50_HZ);
}

uint32_t timer = millis();
uint32_t gpstimer = timer;
void loop()
{

  /*
  char c = GPS.read();
  if (GPS.newNMEAreceived()) {

  if (!GPS.parse(GPS.lastNMEA()))
      return;
  }
  */// Remove this if unnecessary

  if (timer > millis())  timer = millis(); // if millis() or timer wraps around, we'll just reset it
  if (gpstimer > millis())  gpstimer = millis();

  if (millis() - timer >= 35) { // We can prepare and send data approximately every 35 milliseconds (29 Hz). Optimization might allow decrease?
    timer = millis(); // reset the timer

    //ms5
    sensor.ReadProm();
    sensor.Readout();

    //h3lis331
    lis.read();
    lis.getEvent(&event);

    //prepare the data
    data telem;
    if(GPS.fix == 0 or millis()-gpstimer < 100){ // Gps needs to be read at a slower rate (10 Hz). Send garbage values if unavailable.
      telem.latitude = -999.0;
      telem.longitude = -999.0;
      telem.altitude = -999.0;
    }else{
      telem.latitude = GPS.latitudeDegrees;
      telem.longitude = GPS.longitudeDegrees;
      telem.altitude = GPS.altitude;
      gpstimer = millis();
    }
    telem.time = (float)millis();
    telem.accx = event.acceleration.x;
    telem.accy = event.acceleration.y;
    telem.accz = event.acceleration.z;
    telem.mA = ina219.getCurrent_mA();
    telem.V = ina219.getBusVoltage_V() + (ina219.getShuntVoltage_mV() / 1000); //loadVoltage
    telem.temp = sensor.GetTemp();
    telem.pressure = sensor.GetPres();

    //write data to pi via serial
    Serial.write((byte*)&telem, sizeof(data));
  }
}
