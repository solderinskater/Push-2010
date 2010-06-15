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
#ifndef READSENSORS_H_
#define READSENSORS_H_

#include <avr/delay.h>
#include <avr/interrupt.h>
#include <stdlib.h>

#include "bluetooth.h"
#include "io.h"
#include "uart.h"
#include "spi.h"
#include "adxl345.h"

#define SENSOR_COUNT 11 // number of total sensor channels
#define ADC_COUNT 8 // number of adc channels

uint8_t cmd;
uint16_t values[SENSOR_COUNT]; // stores all sensor values
char buffer[10]; // buffer for sprintf/atoi, max 65535+\0+label+:+tab

// labels of all sensor channels
const char sensor_labels[SENSOR_COUNT] = "XYZxyzABCDE";
// which of those channels are ADCs (some are read via SPI)
const uint8_t adc_ids[ADC_COUNT] = {0,1,2,6,7,8,9,10};
// which of those are adxl345 channels
const uint8_t adxl345_ids[3] = {3,4,5};

uint16_t adxl345_values[3];

void init(void);
void sample_adcs(void);
void sample_adxl345(void);
void uart_transfer_battlow(void);
void uart_transfer_values_human_readable(void);
void uart_transfer_values_csv(void);

#endif /* READSENSORS_H_ */
