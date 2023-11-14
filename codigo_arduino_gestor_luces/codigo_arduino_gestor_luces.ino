#include <WiFi.h>
const int sensorPin = A0; // Pin analógico al que está conectado el sensor fotosensible
const int relePin = 13; // Pin digital al que está conectado el relé
int lastSensorValue = 0; // Variable para almacenar la última lectura del sensor
int releState = LOW; // Variable para almacenar el estado actual del relé (inicializado como apagado)

const char* ssid = "wifi_guido";     // Cambia esto con el nombre de tu red Wi-Fi
const char* password = "9dejuliorafaela"; // Cambia esto con tu contraseña de red Wi-Fi


void setup() {
  pinMode(sensorPin, INPUT); // Configura el pin del sensor como entrada
  pinMode(relePin, OUTPUT); // Configura el pin del relé como salida
  Serial.begin(9600); // Inicializa la comunicación serial a 9600 baudios
  Serial.begin(115200);
  delay(1000);

  // Conéctate a la red Wi-Fi
  Serial.println("Conectándose a la red Wi-Fi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Intentando conectar a la red Wi-Fi...");
  }

  Serial.println("Conexión exitosa a la red Wi-Fi");
}


void loop() {
  // Realiza una lectura del sensor cada 3 segundos
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= 3000) {
    previousMillis = currentMillis; // Actualiza el tiempo del último intervalo

    // Lee el valor del sensor fotosensible
    int sensorValue = analogRead(sensorPin);

    // Comprueba si el valor del sensor ha cambiado desde la última lectura y lo muestra por pantalla
    if (sensorValue != lastSensorValue) {
      lastSensorValue = sensorValue;
      Serial.print("Lectura del sensor: ");
      Serial.println(sensorValue);
    }
  }

  // Verifica si hay datos disponibles en el puerto serial (tecla presionada)
  if (Serial.available() > 0) {
    char tecla = Serial.read(); // Lee la tecla presionada
    
    // Cambia el estado del relé cuando se presiona la letra "a"
    if (tecla == 'a' || tecla == 'A') {
      releState = (releState == LOW) ? HIGH : LOW; // Cambia el estado del relé
      digitalWrite(relePin, releState); // Apaga o enciende el relé según el estado
      Serial.print("Estado del relé: ");
      Serial.println(releState == HIGH ? "Encendido" : "Apagado");
    }
  }
}



