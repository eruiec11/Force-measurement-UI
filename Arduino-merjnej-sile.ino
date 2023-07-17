const int napPin = 13;
const int ledPin = 12;
long prejsnjiCas = 0;
const long interval = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(napPin,OUTPUT);
  pinMode(ledPin,OUTPUT);
  digitalWrite(napPin, LOW);
  digitalWrite(ledPin, LOW);

}

void loop() {

  long trenutniCas = millis();
  if(trenutniCas - prejsnjiCas >= interval){
    prejsnjiCas = trenutniCas;

  int vhod = analogRead(A0);
  float napetost = vhod * (5.0 / 1023.0);
  Serial.print(napetost);
  Serial.print((","));
  Serial.println(trenutniCas / 1000.0);
    }

  if(Serial.available()){
      char branjeSerial = Serial.read();
      if(branjeSerial == 's') {
          digitalWrite(napPin, HIGH);
          digitalWrite(ledPin, HIGH);
                
      } 
      else if(branjeSerial == 'p'){
          digitalWrite(napPin, LOW);
          digitalWrite(ledPin, LOW);
      }
   } 
}
