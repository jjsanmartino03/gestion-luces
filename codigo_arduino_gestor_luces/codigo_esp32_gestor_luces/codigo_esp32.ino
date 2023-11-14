#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "wifi_guido";
const char* password = "9dejuliorafaela";

const char* serverName = "http://192.168.174.7:8000/";


int lastSensorValue = 0;
int releState = LOW;

#define RELE_PIN 5 // GPIO 5
#define SENSOR_PIN 36

WebServer server(80);

void setup() {
  Serial.begin(9600);
  delay(1000);

  connectToWiFi();

  pinMode(SENSOR_PIN, INPUT);
  pinMode(RELE_PIN, OUTPUT);

  setupServerRoutes();
  
  server.begin();
  Serial.println("HTTP server started");
}

void connectToWiFi() {
  Serial.println("Conectándose a la red Wi-Fi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Intentando conectar a la red Wi-Fi...");
  }

  Serial.println("Conexión exitosa a la red Wi-Fi");
  Serial.print("Dirección IP asignada: ");
  Serial.println(WiFi.localIP());
}

void setupServerRoutes() {
  server.on("/hola", HTTP_GET, handleHolaRequest);
}

void handleHolaRequest() {
  toggleRelayState();
  server.send(200, "text/plain", "Solicitud recibida");
}

void toggleRelayState() {
  releState = (releState == LOW) ? HIGH : LOW;
  digitalWrite(RELE_PIN, releState);
  Serial.print("Estado del relé: ");
  Serial.println(releState == HIGH ? "Encendido" : "Apagado");
}

void loop() {
  readSensorValue();

  handleSerialInput();

  server.handleClient();
  delay(2);
}

void readSensorValue() {
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= 3000) {
    previousMillis = currentMillis;
    int sensorValue = analogRead(SENSOR_PIN);

    Serial.println(sensorValue);

    if (sensorValue != lastSensorValue) {
      lastSensorValue = sensorValue;
      Serial.print("Lectura del sensor: ");
      Serial.println(sensorValue);
    }
  }
}

void handleSerialInput() {
  if (Serial.available() > 0) {
    char tecla = Serial.read();
    
    if (tecla == 'a' || tecla == 'A') {
      toggleRelayState();
    }
  }
}
