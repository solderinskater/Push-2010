// Copyright 2010 Jan Anlauff <jan at 23t.de>
//
// This file is part of Soldering Skaters Nokia Push Project.
//
// Soldering Skaters Nokia Push Project is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Soldering Skaters Nokia Push Project is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Soldering Skaters Nokia Push Project.  If not, see <http://www.gnu.org/licenses/>.
/*
 * io.h
 */

#ifndef IO_H_
#define IO_H_

#include <avr/pgmspace.h>

// diptera
#define LED_PIN PB2
#define LED_PORT PORTB
#define LED_PORT_REGISTER DDRB

// arduino diecimila
//#define LED_PIN PD5
//#define LED_PORT PORTD
//#define LED_PORT_REGISTER DDRD

// FSR Voltage Divider needs Ground on PB0
#define GROUND_PIN PB0
#define GROUND_PORT PORTB
#define GROUND_PORT_REGISTER DDRB

#define ADC_PORT PORTC
#define ADC_PORT_REGISTER DDRC

void led_init (void);
void led_on(void);
void led_off(void);
void led_toggle(void);
void gnd_init(void);

void adc_init(void);
uint16_t adc_read(uint8_t);

void digital_out_init(void);
void digital_write(uint8_t, uint8_t);

#endif /* IO_H_ */
