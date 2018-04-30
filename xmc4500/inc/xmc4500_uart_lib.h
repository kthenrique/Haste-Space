/*
 * test_uart.h
 *
 *  Created on: 20.09.2016
 *      Author: Markus
 */

#ifndef TEST_UART_H_
#define TEST_UART_H_

#include <stdio.h>
#include <stdarg.h>
#include <stdint.h>

#include <xmc_uart.h>
#include <xmc_gpio.h>

/******************************************************************** GLOBALS */
/******************************************************************** FUNCTION PROTOTYPES */
void _init_uart0_ch0(void);
uint8_t _uart_send_char(char c);
uint8_t _uart_printf(char *fmt, ...);
uint8_t _uart_send_string(char *str);
uint8_t _uart_get_string (char *str);
#endif /* TEST_UART_H_ */

/* EOF */
