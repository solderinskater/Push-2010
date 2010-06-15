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
 * usart.h
 * Interrupt-driven code from http://www.rn-wissen.de/index.php/UART_mit_avr-gcc
 */

#ifndef USART_H_
#define USART_H_

#include <stdio.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include "fifo.h"

#define BAUDRATE 115200UL

// Compatibility Aliases for ATMega168 and friends
#define    UCSRA    UCSR0A
#define    UCSRB    UCSR0B
#define    UCSRC    UCSR0C
#define    UBRRH    UBRR0H
#define    UBRRL    UBRR0L
#define    UDRE     UDRE0
#define    UDR      UDR0
#define    RXC      RXC0
#define    TXC      TXC0
#define    RXCIE    RXCIE0
#define    RXEN     RXEN0
#define    TXEN     TXEN0
#define    UCSZ0    UCSZ00
#define    UCSZ1    UCSZ01
#define    UDRIE    UDRIE0
// ugly fix-code- really fix when it works
#define    SIG_UART_TRANS    SIG_USART_TRANS
#define    SIG_UART_RECV     SIG_USART_RECV
#define    SIG_UART_DATA     SIG_USART_DATA

// old
//void uart_init(unsigned int);
//void uart_transfer(unsigned char);


extern void uart_init(void);
extern int uart_putc (const uint8_t);
int uart_putcs (const uint8_t, FILE *stream);
extern uint8_t uart_getc_wait(void);
extern int uart_getc_nowait(void);
void uart_puts (const char *s);
void uart_puts_P (PGM_P s);

static inline void uart_flush(void);
static inline void uart_flush() {
	while (UCSRB & (1 << UDRIE));
}

#endif /* USART_H_ */
