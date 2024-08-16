#include <stdio.h>
#include <string.h>
#include <getopt.h>
#include <stdlib.h>
#include "irslinger.h"

int main(int argc, char *argv[])
{

	uint32_t outPin = 23;            // The Broadcom pin number the signal will be sent on
	int frequency = 38000;           // The frequency of the IR signal in Hz
	double dutyCycle = 0.5;          // The duty cycle of the IR signal. 0.5 means for every cycle,
	                                 // the LED will turn on for half the cycle time, and off the other half
	int leadingPulseDuration = 9000; // The duration of the beginning pulse in microseconds
	int leadingGapDuration = 4500;   // The duration of the gap in microseconds after the leading pulse
	int onePulse = 562;              // The duration of a pulse in microseconds when sending a logical 1
	int zeroPulse = 562;             // The duration of a pulse in microseconds when sending a logical 0
	int oneGap = 1688;               // The duration of the gap in microseconds when sending a logical 1
	int zeroGap = 562;               // The duration of the gap in microseconds when sending a logical 0
	int sendTrailingPulse = 1;       // 1 = Send a trailing pulse with duration equal to "onePulse"
	                                 // 0 = Don't send a trailing pulse
	char* buttonCode = "01000001101101100101100010100111";

	int opt;

	while ((opt = getopt (argc, argv, "o:l:c:")) != -1) {
		switch (opt) {
			case 'o': //set output pin
				outPin = atoi(optarg);
				break;
			case 'l': //set leading pulse duration (for protocols)
				leadingPulseDuration = atoi(optarg);
				break;
			case 'c': //button code
				buttonCode = optarg;
				buttonCode = buttonCode + '\0';
				//printf("Got code %s\n",buttonCode);
				break;
			default:
				printf("ERROR: Invalid option code\n");
				break;
		}
	}


	int result = irSling(
		outPin,
		frequency,
		dutyCycle,
		leadingPulseDuration,
		leadingGapDuration,
		onePulse,
		zeroPulse,
		oneGap,
		zeroGap,
		sendTrailingPulse,
		buttonCode);
	
	return result;
}
