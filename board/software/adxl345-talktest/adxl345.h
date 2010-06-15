// Copyright 2010 Jan Anlauff <code at 23t.de>
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

#ifndef _ADXL345_H
#define _ADXL345_H

#include <stdio.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/delay.h>

#define ADXL345_PORT_REGISTER DDRB
#define ADXL345_PORT PORTB
#define ADXL345_SS DDB1 //PORTB

#define READ_MASK 0x80 // MSB high for reading 
#define MB_MASK 0x40 // Multiple-byte Mode Mask
#define ADXL345_NOP 0x00

// ADXL345 Register Names, taken from datasheet
#define DEVID 0x00
#define THRESH_TAP 0x1D
#define OFSX 0x1E
#define OFSY 0x1F
#define OFSZ 0x20
#define DUR 0x21
#define Latent 0x22
#define Window 0x23
#define THRESH_ACT 0x24
#define THRESH_INACT 0x25
#define TIME_INACT 0x26
#define ACT_INACT_CTL 0x27
#define THRESH_FF 0x28
#define TIME_FF 0x29
#define TAP_AXES 0x2A
#define ACT_TAP_STATUS 0x2B
#define BW_RATE 0x2C
#define POWER_CTL 0x2D
#define INT_ENABLE 0x2E
#define INT_MAP 0x2F
#define INT_SOURCE 0x30
#define DATA_FORMAT 0x31
#define DATAX0 0x32
#define DATAX1 0x33
#define DATAY0 0x34
#define DATAY1 0x35
#define DATAZ0 0x36
#define DATAZ1 0x37
#define FIFO_CTL 0x38
#define FIFO_STATUS 0x39

#define FOSC 16000000

#define X 0
#define Y 1
#define Z 2

// Delay > 216/FOSC in Mhz is not possible with delay.h functions
#define delay_ms(a){ if (a<216000000/FOSC){ _delay_ms(a); }else{for(uint16_t t=0; t<=a; t++){_delay_ms(1);}}}

uint8_t adxl345_raw_values[6];

// union for 16 bit result value
typedef union {
  uint8_t bytes[2];
  int16_t integer;
} adxl345_value_t;

adxl345_value_t adxl345_value; // union for single value

void adxl345_disable(void);
void adxl345_enable(void);
void adxl345_init(void);
uint8_t adxl345_get_register(uint8_t register_name);
void adxl345_set_register(uint8_t register_name, uint8_t value);
void adxl345_sample(uint16_t* values);

#endif
