#define TRIG D1
#define ECHO D2

#define GREEN_LED D5
#define YELLOW_LED D6
#define RED_LED D7

#define BUZZER D0

String driverState = "ALERT";

void setup() {

  Serial.begin(9600);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  pinMode(BUZZER, OUTPUT);

  Serial.println("SAFE");
}

void loop() {

  // =========================
  // RECEIVE DRIVER STATE
  // =========================

  if (Serial.available()) {

    driverState = Serial.readStringUntil('\n');
    driverState.trim();
  }

  // =========================
  // ULTRASONIC SENSOR
  // =========================

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH);

  float distance = duration * 0.034 / 2;

  // =========================
  // RESET OUTPUTS
  // =========================

  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);

  digitalWrite(BUZZER, LOW);

  // =========================
  // DRIVER DROWSINESS ALERT
  // =========================

  if (driverState == "DROWSY") {

    // DO NOT send DANGER here
    // FCW should remain true to ultrasonic state

    digitalWrite(RED_LED, HIGH);

    digitalWrite(BUZZER, HIGH);
    delay(80);

    digitalWrite(BUZZER, LOW);
    delay(120);
  }

  // =========================
  // FCW DANGER
  // =========================

  else if (distance < 50) {

    Serial.println("DANGER");

    digitalWrite(RED_LED, HIGH);

    digitalWrite(BUZZER, HIGH);
    delay(40);

    digitalWrite(BUZZER, LOW);
    delay(160);
  }

  // =========================
  // FCW WARNING
  // =========================

  else if (distance < 100) {

    Serial.println("WARNING");

    digitalWrite(YELLOW_LED, HIGH);

    digitalWrite(BUZZER, HIGH);
    delay(30);

    digitalWrite(BUZZER, LOW);
    delay(400);
  }

  // =========================
  // SAFE STATE
  // =========================

  else {

    Serial.println("SAFE");

    digitalWrite(GREEN_LED, HIGH);

    delay(200);
  }
}