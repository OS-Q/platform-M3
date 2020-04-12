#include <Arduino.h>

#ifndef LED_BUILTIN
  #define LED_BUILTIN PC13
#endif

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(PIN_SPI_MOSI, OUTPUT);
}

void loop()
{
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(PIN_SPI_MOSI, HIGH);
  // wait for a second
  delay(1000);
  // turn the LED off by making the voltage LOW
  digitalWrite(PIN_SPI_MOSI, LOW);
   // wait for a second
  delay(1000);
}
