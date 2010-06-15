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
 * spi.h - SPI related functions
 */
#ifndef _SPI_H
#define _SPI_H

#include <avr/io.h>
#include <avr/delay.h>
#include <stdio.h>
#include "uart.h"

#define SPI_PORT_REGISTER DDRB
#define SPI_PORT PORTB
#define MOSI PORTB3
#define MISO PORTB4
#define SCK PORTB5

void spi_init_master(void);
//void spi_transfer(uint8_t);
uint8_t spi_transfer_wait(uint8_t);

#endif
