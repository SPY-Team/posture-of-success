#include <WiFi.h>
#include <WiFiUdp.h>

#include "esp32-hal-adc.h" // needed for adc pin reset
#include "soc/sens_reg.h" // needed for adc pin reset
uint64_t reg_b; // Used to store Pin registers

const char* udpAddress = "192.168.0.255";
const int udpPort = 8080;
const char* broadcastMsg = "Hello, world!";

WiFiUDP udp;
WiFiClient client;

int left_back_pin = 26;
int left_hip_pin = 25;
int left_thigh_pin = 27;

int right_back_pin = 32;
int right_hip_pin = 35;
int right_thigh_pin = 33;

int left_back_val;
int left_hip_val;
int left_thigh_val;

int right_back_val;
int right_hip_val;
int right_thigh_val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(left_back_pin, INPUT);
  pinMode(left_hip_pin, INPUT);
  pinMode(left_thigh_pin, INPUT);
  pinMode(right_back_pin, INPUT);
  pinMode(right_hip_pin, INPUT);
  pinMode(right_thigh_pin, INPUT);

  // Save Pin Registers : Do this before begin Wifi
  reg_b = READ_PERI_REG(SENS_SAR_READ_CTRL2_REG);
  
  // setup wifi
  
  //Init WiFi as Station, start SmartConfig
  WiFi.mode(WIFI_AP_STA);
  WiFi.beginSmartConfig();

  //Wait for SmartConfig packet from mobile
  Serial.println("Waiting for SmartConfig.");
  while (!WiFi.smartConfigDone()) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("SmartConfig received.");

  //Wait for WiFi to connect to AP
  Serial.println("Waiting for WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  udp.begin(udpPort);
}

int readForce(int pin) {
  WRITE_PERI_REG(SENS_SAR_READ_CTRL2_REG, reg_b);
  SET_PERI_REG_MASK(SENS_SAR_READ_CTRL2_REG, SENS_SAR2_DATA_INV);
  return analogRead(pin);
}

void loop() {
  // wifi
  Serial.print("Broadcasting: ");
  Serial.println(broadcastMsg);
  udp.beginPacket(udpAddress, udpPort);
  udp.print("Hello, world!");
  udp.endPacket();
  
  uint8_t buffer[50];
  memset(buffer, 0, 50);
  int packetSize;
  if((packetSize = udp.parsePacket()))
  {
    Serial.printf("packet size= %d\n", packetSize);
    udp.read(buffer, 50);
    Serial.print("Got server IP: ");
    Serial.println((char *)buffer);
    for (int i = 0; !client.connect((char*)buffer, 8081); ++i) {
        if (i >= 100) {
          return;
        }
        Serial.println("Connection to host failed, trying again...");
    }
    Serial.printf("Connection to host succeed: %s:%d\n", (char*)buffer, 8081);
    while(true) {
      //Serial.print("Sending data to host...\n");
      left_back_val = readForce(left_back_pin);
      left_hip_val = readForce(left_hip_pin);
      left_thigh_val = readForce(left_thigh_pin);

      right_back_val = readForce(right_back_pin);
      right_hip_val = readForce(right_hip_pin);
      right_thigh_val = readForce(right_thigh_pin);
      
      int nBytes = client.printf("%d, %d, %d, %d, %d, %d\n", left_back_val, left_hip_val, left_thigh_val, right_back_val, right_hip_val, right_thigh_val);
      if (nBytes == 0) {
        return;
      }
      delay(100);
    }
  }

  delay(100);
}
