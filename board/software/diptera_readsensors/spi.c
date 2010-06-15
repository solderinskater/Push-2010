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
 * spi.c
 */

#include "includes/spi.h"

void spi_init_master(void) {
	  // Initialize SPI configuration register
//	  SPCR = (0 << SPIE) | /* SPI Interrupt Enable */
//	         (1 << SPE)  | /* SPI Enable */
//	         (0 << DORD) | /* Data Order: MSB first */
//	         (1 << MSTR) | /* Master mode */
//	         (0 << CPOL) | /* Clock Polarity: SCK low when idle */
//	         (0 << CPHA) | /* Clock Phase: sample on rising SCK edge */
//	         (1 << SPR1) | /* Clock Frequency: f_OSC / 64 */
//	         (0 << SPR0);

//	uint8_t spi_junk;
//
	// Switch MOSI pin to output mode.
	SPI_PORT_REGISTER |= _BV(MOSI);
	SPI_PORT_REGISTER |= _BV(SCK);

	SPCR = (0 << SPIE) | /* SPI Interrupt Enable */
		   (1 << SPE)  | /* SPI Enable */
		   (0 << DORD) | /* Data Order: MSB first */
		   (1 << MSTR) | /* Master mode */
		   (1 << CPOL) | /* Clock Polarity: SCK low when idle */
		   (1 << CPHA) | /* Clock Phase: sample on rising SCK edge */
		   (0 << SPR1) | /* Clock Frequency: f_OSC / 64 */
		   (0 << SPR0);

	// Enable internal pull-ups
//	SPI_PORT |= _BV(MOSI);
//	SPI_PORT |= _BV(MISO);

	_delay_us(1);
}

// Shift out and a received byte of data via SPI
void spi_transfer(uint8_t value) {
	// Start transmission
	SPDR = value;
}

// Shift out and a received byte of data via SPI and wait for its transmission
uint8_t spi_transfer_wait(uint8_t value) {
	// Start transmission
	SPDR = value;
	/* Wait for transmission complete */
	while(!(SPSR & (1<<SPIF))) {
		;
	}
	return SPDR;
}
