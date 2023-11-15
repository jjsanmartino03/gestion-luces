#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

const char* ssid = "Fibertel WiFi220 2.4GHz";
const char* password = "01423429989";

const char* serverName = "http://192.168.0.66:8000/api/registro_sensores/";


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
  char* request= toggleRelayState();
  server.send(200, "text/plain", request);
}

char* toggleRelayState() {
  releState = (releState == LOW) ? HIGH : LOW;
  digitalWrite(RELE_PIN, releState);
  char* changeState = readSensorRightNow();
  Serial.print("Estado del relé: ");
  Serial.println(releState == HIGH ? "Encendido" : "Apagado");
  return changeState;
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

  if (currentMillis - previousMillis >= 10000) {
    previousMillis = currentMillis;
    int sensorValue = analogRead(SENSOR_PIN);

    Serial.println(sensorValue);

    // valor máximo 4096 (apagado)
    // valor mínimo 0 (prendido)
    int digitalSensorValue = (sensorValue > 1800) ? 0 : 1;
    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    String httpRequestData = "estado=";
    httpRequestData += digitalSensorValue;
    // Send HTTP POST request
    int httpResponseCode = http.POST(httpRequestData);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // Free resources
    http.end();

    if (sensorValue != lastSensorValue) {
      lastSensorValue = sensorValue;
      Serial.print("Lectura del sensor: ");
      Serial.println(sensorValue);
      Serial.println("Lectura digital: ");
      Serial.println(digitalSensorValue);

    }
  }
}


char* readSensorRightNow(){
  int sensorValue = analogRead(SENSOR_PIN);
  if (sensorValue>1800){
    return "0";
  }
  else {
    return "1";
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
