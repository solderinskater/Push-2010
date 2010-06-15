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
 * bluetooth.h - Definitions related to RN-41 Bluetooth Module
 */


#include <avr/io.h>
#include <avr/delay.h>


#ifndef BLUETOOTH_H_
#define BLUETOOTH_H_

// reset pin
#define BT_RESET_PIN PD3
#define BT_RESET_PORT PORTD
#define BT_RESET_PORT_REGISTER DDRD

// connected pin
#define BT_CONN_PIN PD2
#define BT_CONN_PORT PIND
#define BT_CONNECTED 1

#define BT_RESET_TIME 50 // ms

void bluetooth_init(void);
void bluetooth_reset(void);
uint8_t bluetooth_connected(void);

#endif /* BLUETOOTH_H_ */
