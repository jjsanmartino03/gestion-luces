const int sensorPin = 26; // Pin analógico al que está conectado el sensor fotosensible (pin 26 en ESP-WROOM-32)
const int relePin = 33; // Pin digital al que está conectado el relé (pin 33 en ESP-WROOM-32)
int lastSensorValue = 0; // Variable para almacenar la última lectura del sensor
int releState = LOW; // Variable para almacenar el estado actual del relé (inicializado como apagado)

void setup() {
  pinMode(sensorPin, INPUT); // Configura el pin del sensor como entrada
  pinMode(relePin, OUTPUT); // Configura el pin del relé como salida
  Serial.begin(9600); // Inicializa la comunicación serial a 9600 baudios
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
