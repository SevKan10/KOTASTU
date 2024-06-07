void Connected(){
  while(bleMouse.isConnected()) {
   while(Serial2.available()) {
 
    A = Serial2.readStringUntil('\n');
    
    x = splitString(A, ",", 1).toInt();
    y = splitString(A, ",", 2).toInt();
    
    if(digitalRead(Left) == 0) {bleMouse.press(MOUSE_LEFT);}
    if(digitalRead(Left) != 0) {bleMouse.release(MOUSE_LEFT);}
    
    if(digitalRead(Right) == 0) {bleMouse.press(MOUSE_RIGHT);}
    if(digitalRead(Right) != 0) {bleMouse.release(MOUSE_RIGHT);}
    
    bleMouse.move(x, y, z); delay(5);
    
  }
  while(!Serial2.available()){ 
  
    if(digitalRead(Left) == 0) {bleMouse.press(MOUSE_LEFT);}
    if(digitalRead(Left) != 0) {bleMouse.release(MOUSE_LEFT);}
    
    if(digitalRead(Right) == 0) {bleMouse.press(MOUSE_RIGHT);}
    if(digitalRead(Right) != 0) {bleMouse.release(MOUSE_RIGHT);}
    
    x = 0; y = 0; z = 0;
    bleMouse.move(x, y, z); delay(5); 
    }
    
    if (interruptFlag) {
    Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
    bleMouse.end();
    Serial.println("state 1");
    state = 1;
    delay(300);
    interruptFlag = false;
    return loop();
     
  }
 }
}

String splitString(String inputString, String delim, uint16_t pos){
String tmp = inputString;
  for(int i=0; i<pos; i++){
    tmp = tmp.substring(tmp.indexOf(delim)+1);
    if(tmp.indexOf(delim)== -1 
    && i != pos -1 )
      return "";
  }
  return tmp.substring(0,tmp.indexOf(delim));
}
