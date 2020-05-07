#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "Sogang ICPC Team";
const char* pwd = "sogang512";

const char* udpAddress = "192.168.0.255";
const int udpPort = 8080;
const char* broadcastMsg = "Hello, world!";

WiFiUDP udp;
WiFiClient client;

void setup(){
  Serial.begin(115200);
   WiFi.begin(ssid, pwd);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  udp.begin(udpPort);
}

void loop(){
  Serial.print("Broadcasting: ");
  Serial.println(broadcastMsg);
  udp.beginPacket(udpAddress, udpPort);
  udp.print("Hello, world!");
  udp.endPacket();
  
  uint8_t buffer[50] = "hello world";
  memset(buffer, 0, 50);
  udp.parsePacket();
  if(udp.read(buffer, 50) > 0){
    Serial.print("Got server IP: ");
    Serial.println((char *)buffer);
    if (!client.connect((char*)buffer, 8080)) {
        Serial.println("Connection to host failed");
        return;
    }
    Serial.print("Connection to host succeed: ");
    Serial.print((char*)buffer);
    Serial.print(8080);
    while(true) {
      client.print("Some data");
      delay(1000);
    }
  }
  delay(1000);
}
