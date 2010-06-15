/*
	ADXL345 Accelerometer test code
	
	Copyright 2010 Jan Anlauff <code at 23t.de>
	Adapted from Viliam Klein's Example (c) 2009
*/
// This file is part of the Soldering Skaters Nokia Push Project
// (short: the project).
// 
// The project is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// The project is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with the project.  If not, see <http://www.gnu.org/licenses/>.
/*	
	This code sets up the power and mode registers and then prints out the data registers forever.
	UART is set to 19200 8N1
	
	using ATMega328 on Seeeduino, 3.3V / 16 Mhz 8MHz board

	Todos:
		* Understand specific commands
		* Fix ms/us delays
*/

#include <stdio.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/delay.h>

#include "adxl345.h"

#define BAUD 9600
#define MYUBRR 103

#define sbi(var, mask)	 ((var) |= (uint8_t)(1 << mask))
#define cbi(var, mask)	 ((var) &= (uint8_t)~(1 << mask))

//ADXL345
#define adxl 2 //PORTB
#define mosi 3 //PORTB
#define sck  5 //PORTB

//Define functions
//======================
void ioinit(uint8_t baud);	  //Initializes IO
//void delay_ms(uint16_t x); //General purpose delay

static int uart_putchar(char c, FILE *stream);
uint8_t uart_getchar(void);
static FILE mystdout = FDEV_SETUP_STREAM(uart_putchar, NULL, _FDEV_SETUP_WRITE);


void iniSPI(void);
uint8_t spi_transfer_wait(uint8_t value);
void resetCS(uint16_t delay);


//======================


int main (void) {
	ioinit(103);
	iniSPI();
	
	printf("\nStart\n");
	
	adxl345_init();

	printf("data is: ");
	
	uint16_t adxl345_values[3];
	while(1) {
	printf("\n");
	
		adxl345_sample(&adxl345_values);
		printf("X%6d\tY%6d\tZ%6d", adxl345_values[X], adxl345_values[Y], adxl345_values[Z]);
		/*
		for(int i=0; i<3; i++) {
			printf("%d ",adxl345_values[i]);
//		printf("%x ",adxl345_raw_values[i]);
		}
		*/
		_delay_ms(4);
	}
	
	return(0);
}

uint8_t spi_transfer_wait(uint8_t value) {
	// Start transmission
	SPDR = value;
	/* Wait for transmission complete */
	while(!(SPSR & (1<<SPIF))) {
		;
	}
	return SPDR;
}

void iniSPI(void)
{
	// Set MOSI, SCK, and SS output, all others input 
	sbi(DDRB, adxl);	//acc1 cs output
	sbi(PORTB, adxl);

	sbi(DDRB, mosi);
	sbi(DDRB, sck);
	
	cbi(SPCR, CPHA);
	SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR1)|(1<<SPR0)|(1<<CPHA)|(1<<CPOL);
	cbi(SPCR, SPR1);
	cbi(SPCR, SPR0);
	//sbi(SPSR, 0);
	_delay_us(1);
}


void ioinit (uint8_t baud)
{
	//1 = output, 0 = input
	//DDRB = 0b11110100; //All inputs
	DDRB = 0b11101111; //All inputs
	//sbi(DDRB, adxl);	//acc1 cs output
	//sbi(DDRB, mosi);
	//sbi(DDRB, sck);
	DDRC = 0b11111111; //All outputs
	DDRD = 0b11001110;  //PORTD (RX on PD0)
	//DDRA = 0b11111111;
	//CLKPR = (1 << CLKPCE);
	//CLKPR = (3<<CLKPS);
	
	UBRR0H = MYUBRR >> 8;
	UBRR0L = MYUBRR;
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	UCSR0A = (1<<U2X0);		
		
	stdout = &mystdout; //Required for printf init

}

static int uart_putchar(char c, FILE *stream)
{
	if (c == '\n') uart_putchar('\r', stream);
	loop_until_bit_is_set(UCSR0A, UDRE0);
	UDR0 = c;
	
	return 0;
}

uint8_t uart_getchar(void)
{
	while( !(UCSR0A & (1<<RXC0)) );
	return(UDR0);
}
