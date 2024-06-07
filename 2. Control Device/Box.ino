#define BLYNK_PRINT Serial

#define BLYNK_TEMPLATE_ID "TMPL6gkwkeRiZ"
#define BLYNK_TEMPLATE_NAME "FOOT MOUSE"
#define BLYNK_AUTH_TOKEN "s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH"

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

#include <NTPClient.h>
#include <WiFiUdp.h>
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");
//-----------------------------------------------------------------------
#include <Wire.h>
#include "RTClib.h"
RTC_DS1307 rtc;e

char ssid[] = "THIEN TRANG";
char pass[] = "phucnhannghia";

int Device[] = {12,13,14,33,26,27,25,32};
unsigned long TIme;

int h_on,m_on;
int h_off,m_off;
int device;
String state;

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200);
  
  Wire.begin(23,22);
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }
  
  
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  timeClient.begin();
  timeClient.setTimeOffset(25200);

  timeClient.update();
  int h = timeClient.getHours();
  int m = timeClient.getMinutes();
  int s = timeClient.getSeconds();

  rtc.adjust(DateTime(2024, 5, 24, h, m, s));
  
  pinMode(Device[0],OUTPUT);
  pinMode(Device[1],OUTPUT);
  pinMode(Device[2],OUTPUT);
  pinMode(Device[3],OUTPUT);
  pinMode(Device[4],OUTPUT);
  pinMode(Device[5],OUTPUT);
  pinMode(Device[6],OUTPUT);
  pinMode(Device[7],OUTPUT);

  pinMode(2,OUTPUT); digitalWrite(2,LOW);
  for(int i = 0; i < 10; i++){
    digitalWrite(2,HIGH);
    delay(500);
    digitalWrite(2,LOW);
    delay(500);
  }
  pinMode(2,OUTPUT); digitalWrite(2,LOW);
}

void loop() {
  Blynk.run();
  if(millis() - TIme >= 1000){
    Blynk.syncVirtual(V4);
    TIme = millis();
  }
  Timer();
}

BLYNK_WRITE(V3){
  String Val = param.asString();
  h_on  = splitString(Val,",",2).toInt();
  m_on  = splitString(Val,",",3).toInt();
  h_off = splitString(Val,",",4).toInt();
  m_off = splitString(Val,",",5).toInt();
 device = splitString(Val,",",6).toInt();
  state = splitString(Val,",",1);
  Serial.print(h_on); Serial.print(", ");
  Serial.print(m_on); Serial.print(", ");
  Serial.print(h_off); Serial.print(", ");
  Serial.print(m_off); Serial.print(", ");
  Serial.print(device); Serial.println(", ");
}

BLYNK_WRITE(V2){ // SDT
  String Val = param.asString();
  String X = splitString(Val,",",1);
  call(X);
}
BLYNK_WRITE(V0){
  String Val = param.asString();
  Serial.println(Val);
  if( Val == "On1")  { digitalWrite(Device[0],HIGH); }
  if( Val == "Off1") { digitalWrite(Device[0],LOW); }

  if( Val == "On2")  { digitalWrite(Device[1],HIGH); }
  if( Val == "Off2") { digitalWrite(Device[1],LOW); }

  if( Val == "On3")  { digitalWrite(Device[2],HIGH); }
  if( Val == "Off3") { digitalWrite(Device[2],LOW); }

  if( Val == "On4")  { digitalWrite(Device[3],HIGH); }
  if( Val == "Off4") { digitalWrite(Device[3],LOW); }

  if( Val == "On5")  { digitalWrite(Device[4],HIGH); }
  if( Val == "Off5") { digitalWrite(Device[4],LOW); }

  if( Val == "On6")  { digitalWrite(Device[5],HIGH); }
  if( Val == "Off6") { digitalWrite(Device[5],LOW); }

  if( Val == "On7")  { digitalWrite(Device[6],HIGH); }
  if( Val == "Off7") { digitalWrite(Device[6],LOW); }

  if( Val == "On8")  { digitalWrite(Device[7],HIGH); }
  if( Val == "Off8") { digitalWrite(Device[7],LOW); }
}

String splitString(String inputString, String delim, uint16_t pos)
{ String tmp = inputString;
  for(int i = 0; i < pos; i++)
    { tmp = tmp.substring(tmp.indexOf(delim)+1);
      if(tmp.indexOf(delim) == -1 and i != pos-1) return "";
    }
  return tmp.substring(0,tmp.indexOf(delim));
}

void call(String sdt)
{
  Serial2.print(F("ATD"));
  updateSerial();
  Serial.println("Đang Thực Hiện Cuộc Gọi");
  Serial2.print(sdt);
  updateSerial();
  Serial2.print(F(";\r\n"));
  Bip(100, 100);
  Serial2.print(F("ATH"));
  updateSerial();
  Serial2.print(F(";\r\n"));
  updateSerial();
  delay(1000);
  digitalWrite(2,LOW);   
}

void updateSerial()
{
 delay(500);
}

void Bip(int A, int D)
{
 for(int i = 0; i <= A; i++) {digitalWrite(2,1); delay(D); digitalWrite(2,0); delay(D);}
}

void Timer(){ DateTime now = rtc.now();
  Serial.print(now.hour()); Serial.print("   "); Serial.println(now.minute());
  if(now.hour() == h_on  and now.minute() == m_on)  { digitalWrite(Device[device],HIGH); }
  if(now.hour() == h_off and now.minute() == m_off) { digitalWrite(Device[device],LOW); }
}
