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
 * RN 41 related code
 */

#include "includes/bluetooth.h"

void bluetooth_init(void) {
	BT_RESET_PORT_REGISTER |= _BV(BT_RESET_PIN);
	BT_RESET_PORT |= _BV(BT_RESET_PIN);
	bluetooth_reset();
}

void bluetooth_reset(void) {
	// toggle to low for BT_RESET_TIME
	BT_RESET_PORT  &= ~_BV(BT_RESET_PIN);
	_delay_ms(BT_RESET_TIME);
	BT_RESET_PORT |= _BV(BT_RESET_PIN);
}

uint8_t bluetooth_connected(void) {
	if ( BT_CONN_PORT & (1<<BT_CONN_PIN) ) {
		return BT_CONNECTED;
	} else {
		return 0;
	}
}
