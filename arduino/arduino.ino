#include <WiFi.h>
#include <WiFiUdp.h>
#include <EEPROM.h>

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

bool testWifi(void)
{
  int c = 0;
  Serial.println("Waiting for Wifi to connect");
  while ( c < 20 ) {
    if (WiFi.status() == WL_CONNECTED)
    {
      return true;
    }
    delay(500);
    Serial.print("*");
    c++;
  }
  Serial.println("");
  Serial.println("Connect timed out, opening AP");
  return false;
}

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
  EEPROM.begin(512); //Initialasing EEPROM

  Serial.println("Reading EEPROM ssid");

  String esid;
  for (int i = 0; i < 32; ++i) {
    esid += char(EEPROM.read(i));
  }
  Serial.println();
  Serial.print("SSID: ");
  Serial.println(esid);
  Serial.println("Reading EEPROM pass");

  String epass = "";
  for (int i = 32; i < 96; ++i) {
    epass += char(EEPROM.read(i));
  }
  Serial.print("PASS: ");
  Serial.println(epass);

  bool rewrite = false;

  WiFi.begin(esid.c_str(), epass.c_str());
  if (testWifi()) {
    Serial.println("Succesfully Connected!!!"); 
  }
  else {
    rewrite = true;
    
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
  }

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

  if (rewrite) {
    String qsid = WiFi.SSID();
    String qpass = WiFi.psk();

    Serial.println("clearing eeprom");
    for (int i = 0; i < 96; ++i) {
      EEPROM.write(i, 0);
    }
    Serial.println(qsid);
    Serial.println("");
    Serial.println(qpass);
    Serial.println("");

    Serial.println("writing eeprom ssid:");
    for (int i = 0; i < qsid.length(); ++i)
    {
      EEPROM.write(i, qsid[i]);
      Serial.print("Wrote: ");
      Serial.println(qsid[i]);
    }
    Serial.println("writing eeprom pass:");
    for (int i = 0; i < qpass.length(); ++i)
    {
      EEPROM.write(32 + i, qpass[i]);
      Serial.print("Wrote: ");
      Serial.println(qpass[i]);
    }
    EEPROM.commit();
  }
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
      int left_back_val = readForce(left_back_pin);
      int left_hip_val = readForce(left_hip_pin);
      int left_thigh_val = readForce(left_thigh_pin);

      int right_back_val = readForce(right_back_pin);
      int right_hip_val = readForce(right_hip_pin);
      int right_thigh_val = readForce(right_thigh_pin);
      
      int nBytes = client.printf("%d, %d, %d, %d, %d, %d\n", left_back_val, left_hip_val, left_thigh_val, right_back_val, right_hip_val, right_thigh_val);
      if (nBytes == 0) {
        return;
      }
      delay(100);
    }
  }

  delay(100);
}
