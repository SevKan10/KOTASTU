// A0 Si lanh 2 || 1023 kéo ghế lên (0 HIGH, 1 LOW)
// A1 Si lanh 3 || 1023 nâng lên (2 HIGH, 3 LOW)
// A2 Si lanh 1 || 1023 ngã ghế xuống (4 HIGH, 5 LOW)

int A[]={7,8,9,10,11,12};
void setup() {
  Serial.begin(9600);
  for(int i = 0; i < 7; i++){
    pinMode(A[i],OUTPUT);
  }
  for(int i = 0; i < 7; i++){
    digitalWrite(A[i],0);
  }
}

void loop() {
//  for(int i = 0; i < 7; i++){
//    digitalWrite(A[i],1);
//    delay(1000);
//}
  Serial.print(analogRead(A0)); Serial.print(" / ");
  Serial.print(analogRead(A1)); Serial.print(" / ");
  Serial.print(analogRead(A2)); Serial.print(" / ");
  Serial.print(analogRead(A3)); Serial.println(" / ");
  
  if(analogRead(A2) >= 600) {
    digitalWrite(A[4], HIGH);
    digitalWrite(A[5], LOW);
  }
  if(analogRead(A2) <= 400) {
    digitalWrite(A[4], LOW);
    digitalWrite(A[5], HIGH);
  }
  if(analogRead(A2) >= 400 and analogRead(A2) <= 600) {
    digitalWrite(A[4], LOW);
    digitalWrite(A[5], LOW);
  }

  if(analogRead(A1) >= 600) {
    digitalWrite(A[2], HIGH);
    digitalWrite(A[3], LOW);
  }
  if(analogRead(A1) <= 400) {
    digitalWrite(A[2], LOW);
    digitalWrite(A[3], HIGH);
  }
  if(analogRead(A1) >= 400 and analogRead(A1) <= 600) {
    digitalWrite(A[2], LOW);
    digitalWrite(A[3], LOW);
  }

  if(analogRead(A0) >= 600) {
    digitalWrite(A[0], HIGH);
    digitalWrite(A[1], LOW);
  }
  if(analogRead(A0) <= 400) {
    digitalWrite(A[0], LOW);
    digitalWrite(A[1], HIGH);
  }
  if(analogRead(A0) >= 400 and analogRead(A0) <= 600) {
    digitalWrite(A[0], LOW);
    digitalWrite(A[1], LOW);
  }
}
