#include <WiFi.h>
#include <WiFiUdp.h>

#include "esp32-hal-adc.h" // needed for adc pin reset
#include "soc/sens_reg.h" // needed for adc pin reset
uint64_t reg_b; // Used to store Pin registers

const char* ssid = "Sogang ICPC Team";
const char* pwd = "sogang512";

const char* udpAddress = "192.168.0.255";
const int udpPort = 8080;
const char* broadcastMsg = "Hello, world!";

WiFiUDP udp;
WiFiClient client;

int pin = 25;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(pin, INPUT);

  // Save Pin Registers : Do this before begin Wifi
  reg_b = READ_PERI_REG(SENS_SAR_READ_CTRL2_REG);

  // setup wifi
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

float readForce(int pin) {
  // ADC Pin Reset: Do this before every analogRead()
  WRITE_PERI_REG(SENS_SAR_READ_CTRL2_REG, reg_b);
  //VERY IMPORTANT: DO THIS TO NOT HAVE INVERTED VALUES!
  SET_PERI_REG_MASK(SENS_SAR_READ_CTRL2_REG, SENS_SAR2_DATA_INV);

  // put your main code here, to run repeatedly:
  float val = analogRead(pin) / 4096.0f;
  val = (exp(val) - 1) / 1.718f;
  return val;
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
    while (!client.connect((char*)buffer, 8081)) {
        Serial.println("Connection to host failed, trying again...");
    }
    Serial.printf("Connection to host succeed: %s:%d\n", (char*)buffer, 8081);
    while(true) {
      Serial.print("Sending data to host...\n");
      client.printf("%.5f", readForce(pin));
      delay(100);
    }
  }

  delay(100);
}
