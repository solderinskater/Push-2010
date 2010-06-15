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
 * readsensors - Samples analog and digital values
 *               and transmits them via UART/Bluetooth.
 *
 * Todos:

 *  - Test SPI+Accelerometer
 *  - Add Timestamp
 *  - BT init channel
 *  - Add Battery Status
 *  - Add Power-Down Circuitry
 * ----- done ------
 * 	- Add BT init
 *  - Test Serial
 *  - Test ADC
 *  - Test Gyros
 */
#include "includes/diptera_readsensors.h"

int main(void) {
	init();
	while (1) {
		sample_adcs();
		sample_adxl345();
		if (bluetooth_connected()) {
			led_on();
			uart_transfer_values_csv();
			led_off();
		}
		_delay_ms(20);
	}
}


void init(void) {
	led_init();
	led_off();
	sei(); // Turn on interrupts
	uart_init();
	FILE uart_str = FDEV_SETUP_STREAM(uart_putcs, NULL, _FDEV_SETUP_RW);
	stdout = &uart_str;
	adc_init();
	spi_init_master();
	digital_out_init();
	bluetooth_init();
	adxl345_init();
	led_on();
}


void sample_adcs() {
	for(uint8_t adc_id = 0; adc_id < ADC_COUNT; adc_id++) {
		values[adc_ids[adc_id]] = adc_read(adc_id);
	}
}

void sample_adxl345(void) {
	adxl345_sample(&adxl345_values);
	for(uint8_t axis=0; axis < 3; axis++) {
		values[adxl345_ids[axis]] = adxl345_values[axis];
	}
}

void uart_transfer_values_human_readable(void) {
	for (uint8_t sensor_id = 0; sensor_id < SENSOR_COUNT; sensor_id++) {
		sprintf(buffer,"%c: %6d\t",sensor_labels[sensor_id], values[sensor_id]);
		uart_puts(buffer);
	}
	uart_puts("\r\n");
	uart_flush();
}

void uart_transfer_values_csv(void) {
	for (uint8_t sensor_id = 0; sensor_id < SENSOR_COUNT; sensor_id++) {
		itoa(values[sensor_id], buffer, 10);
		uart_puts(buffer);
		uart_puts(",");
	}
	uart_puts("\r\n");
	uart_flush();
}

