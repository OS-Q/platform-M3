#include "mbed.h"

DigitalOut myled(SPI_MISO);

int main() 
{
    while(1) 
    {
        myled = 1;
        wait(1);
        myled = 0;
        wait(1);
    }
}