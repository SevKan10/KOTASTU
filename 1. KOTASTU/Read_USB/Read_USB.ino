#define DEBUG_ALL
#define FORCE_TEMPLATED_NOPS
#include <ESP32-USB-Soft-Host.h>
  // default pins tested on ESP32-Wroom
  #define PROFILE_NAME "Default Wroom"
  #define DP_P0  17  // always enabled
  #define DM_P0  16  // always enabled

String X;

static void my_USB_DetectCB( uint8_t usbNum, void * dev )
{
}

static void my_USB_PrintCB(uint8_t usbNum, uint8_t byte_depth, uint8_t* data, uint8_t data_len)
{
  // if( myListenUSBPort != usbNum ) return;
  for(int k=0;k<data_len;k++) {
    X += String(data[k]) + ",";
  }
  Serial.println(X);
  X ="";
}

usb_pins_config_t USB_Pins_Config =
{
  DP_P0, DM_P0,
};


void setup()
{
  Serial.begin(115200);
  delay(5000);
  //bleMouse.begin();
  printf("USB Soft Host Test for %s\n", PROFILE_NAME );
  printf("TIMER_BASE_CLK: %d, TIMER_DIVIDER:%d, TIMER_SCALE: %d\n", TIMER_BASE_CLK, TIMER_DIVIDER, TIMER_SCALE );
  USH.setOnConfigDescCB( Default_USB_ConfigDescCB );
  USH.setOnIfaceDescCb( Default_USB_IfaceDescCb );
  USH.setOnHIDDevDescCb( Default_USB_HIDDevDescCb );
  USH.setOnEPDescCb( Default_USB_EPDescCb );
  USH.init( USB_Pins_Config, my_USB_DetectCB, my_USB_PrintCB );
}

void loop()
{
  //vTaskDelete(NULL);
}
