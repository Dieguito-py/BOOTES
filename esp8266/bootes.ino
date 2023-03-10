#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "DHTesp.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Wire.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
 
TinyGPSPlus gps;
SoftwareSerial gpsSerial(D1, D2);
char buffer[100];
DHTesp dht;
Adafruit_BMP280 bmp; 

float altitude_base = 1015.25;
float atitude, ongitude;
int ssecond;
String latstr , lngstr, ssecondstr; 
float temperature = 0; 
float pressure = 0; 
float altitude = 0; 

int counter = 0;

const char* ssid = "Amarildo"; 
const char* password = "a2s4f7d22"; 
 
// config static IP
IPAddress ip(192, 168, 1, 100); 
IPAddress gateway(192, 168, 1, 1); 
IPAddress subnet(255, 255, 255, 0); 

ESP8266WebServer server(80);

void setup() {
  gpsSerial.begin(9600);
  dht.setup(14, DHTesp::DHT11); // D5
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  
  WiFi.config(ip, gateway, subnet, gateway);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  Wire.begin(0,2);
  Wire.setClock(100000);

  if (!bmp.begin(0x76)) {
    while (1);
  }

  server.begin();

  server.on("/dados", handleGetPressure);
  server.on("/gps", handleGps);
  delay(2000);
}

void loop() { 
    while (gpsSerial.available() > 0) {
        if (gps.encode(gpsSerial.read())) {
            handleGps();
        }
    }
  server.handleClient();
  delay(50);
  counter++;
  if(counter > 100) {
    getSensorValues(); 
    counter = 0; 
 }    
}

void handleGetPressure() {
  String temperature = String(dht.getTemperature());
  String umidade = String(dht.getHumidity());
  String pressure = String(bmp.readPressure()/101325, 2);
//  hpc
//  String pressure = String(bmp.readPressure()/101325, 2); 
  String altitude = String(bmp.readAltitude(altitude_base));
  server.send(200, "text/html", temperature+"e"+umidade+"e"+pressure+"e"+altitude);
}

void handleGps() {
    if (gps.location.isUpdated()) {
        double lat = gps.location.lat();
        double lng = gps.location.lng();
        latstr = String(lat, 6);
        lngstr = String(lng, 6);
        server.send(200, "text/html", latstr+"e"+lngstr);
    }
}

void getSensorValues() {

  float l = gps.location.lng();
  float w = gps.location.lat();
  float u = dht.getHumidity();
  float t = dht.getTemperature();
  float p = bmp.readPressure();
  float a = bmp.readAltitude(altitude_base); 
  
  if (!isnan(t) && !isnan(p) && !isnan(a)){
    temperature = t;
    pressure = p;
    altitude = a;    
  }
}
