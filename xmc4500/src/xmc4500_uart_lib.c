/*
 * test_uart.c
 *
 *  Created on: 20.09.2016
 *      Author: Markus (MODIFIED BY: Kelve Torres Henrique)
 */
/******************************************************************** LIBS */
#include <xmc4500_uart_lib.h>
/******************************************************************** DEFINES */
#define UART_TX P1_5
#define UART_RX P1_4

#define RX_FIFO_INITIAL_LIMIT 0
#define TX_FIFO_INITIAL_LIMIT 0

#define BUFFER_SIZE_PRINTF 255
#define BUFFER_SIZE_RX 64
#define STRING_LF 10
#define STRING_CR 13

#define ERR_OUT_OF_MEMORY 100
/******************************************************************** GLOBALS */
_Bool str_available = false;
char rx_buffer[BUFFER_SIZE_RX] = {0};
/***************************************************************** STRUCTURES */
XMC_GPIO_CONFIG_t uart_tx = {
	.mode = XMC_GPIO_MODE_OUTPUT_PUSH_PULL_ALT2,
	.output_strength = XMC_GPIO_OUTPUT_STRENGTH_MEDIUM
};

XMC_GPIO_CONFIG_t uart_rx = {
	.mode = XMC_GPIO_MODE_INPUT_TRISTATE
};

XMC_UART_CH_CONFIG_t uart_config = {
	.data_bits = 8U,
	.stop_bits = 1U,
	.baudrate = 115200U
};
/****************************************************************** FUNCTIONS */
void _init_uart0_ch0()
{
	/* USIC channels initialization */
	XMC_UART_CH_Init (XMC_UART0_CH0, &uart_config);

	XMC_UART_CH_SetInputSource (XMC_UART0_CH0, XMC_UART_CH_INPUT_RXD,
				    USIC0_C0_DX0_P1_4);

	/* FIFOs initialization for both channels:
	 *  8 entries for TxFIFO from point 0, LIMIT=1
	 *  8 entries for RxFIFO from point 8, LIMIT=7 (SRBI is set if all 8*data have
	 *                                              been received)
	 *  */
	XMC_USIC_CH_TXFIFO_Configure (XMC_UART0_CH0, 0, XMC_USIC_CH_FIFO_SIZE_8WORDS, TX_FIFO_INITIAL_LIMIT);
	XMC_USIC_CH_RXFIFO_Configure (XMC_UART0_CH0, 8, XMC_USIC_CH_FIFO_SIZE_8WORDS, RX_FIFO_INITIAL_LIMIT);

	/* Enabling events for TX FIFO and RX FIFO */
	XMC_USIC_CH_RXFIFO_EnableEvent (XMC_UART0_CH0,
					XMC_USIC_CH_RXFIFO_EVENT_CONF_STANDARD |
					XMC_USIC_CH_RXFIFO_EVENT_CONF_ALTERNATE);

	/* Connecting the previously enabled events to a Service Request line number */
	XMC_USIC_CH_RXFIFO_SetInterruptNodePointer (XMC_UART0_CH0, XMC_USIC_CH_RXFIFO_INTERRUPT_NODE_POINTER_STANDARD, 0);
	XMC_USIC_CH_RXFIFO_SetInterruptNodePointer (XMC_UART0_CH0, XMC_USIC_CH_RXFIFO_INTERRUPT_NODE_POINTER_ALTERNATE, 0);

	/* Start USIC operation as UART */
	XMC_UART_CH_Start (XMC_UART0_CH0);

	/*Initialization of the necessary ports*/
	XMC_GPIO_Init (UART_TX, &uart_tx);
	XMC_GPIO_Init (UART_RX, &uart_rx);

	/* Configuring priority and enabling NVIC IRQ for the defined service request
	line number */
	NVIC_SetPriority (USIC0_0_IRQn, 63U);
	NVIC_EnableIRQ (USIC0_0_IRQn);

	return;
}

void USIC0_0_IRQHandler (void)
{
	static uint8_t rx_ctr = 0;
	uint8_t rx_tmp = 0;

	/* Read the RX FIFO till it is empty */
	while (!XMC_USIC_CH_RXFIFO_IsEmpty (XMC_UART0_CH0)) {
		rx_tmp = XMC_UART_CH_GetReceivedData (XMC_UART0_CH0);

		if ( (rx_tmp != STRING_CR) && (!str_available)) {
			rx_buffer[rx_ctr++] = rx_tmp;
		} else {
			rx_ctr = 0;
			str_available = true;
		}
	}
}

uint8_t _uart_send_char (char c)
{
	while (XMC_USIC_CH_GetTransmitBufferStatus (XMC_UART0_CH0) == XMC_USIC_CH_TBUF_STATUS_BUSY);
	XMC_UART_CH_Transmit (XMC_UART0_CH0, c);

	return 0;
}

uint8_t _uart_printf (char *fmt, ...)
{
	va_list arg_ptr;
	char buffer[BUFFER_SIZE_PRINTF];

	if (fmt == NULL)  {
		return ERR_OUT_OF_MEMORY;
	}

	va_start (arg_ptr, fmt);
	vsprintf (buffer, fmt, arg_ptr);
	va_end (arg_ptr);

	_uart_send_string (buffer);
	return 0;
}

uint8_t _uart_send_string (char *str)
{
	if (str == NULL) {
		return ERR_OUT_OF_MEMORY;
	}

	for (int i = 0; i < strlen (str); i++) {
		while (XMC_USIC_CH_GetTransmitBufferStatus (XMC_UART0_CH0) == XMC_USIC_CH_TBUF_STATUS_BUSY);
		XMC_UART_CH_Transmit (XMC_UART0_CH0, str[i]);
	}
	return 0;
}

uint8_t _uart_get_string (char *str)
{
	if (str == NULL) {
		return ERR_OUT_OF_MEMORY;
	}

	while (!str_available);
	memcpy (str, &rx_buffer, strlen (rx_buffer));
	memset (&rx_buffer, 0x00, BUFFER_SIZE_RX);

	str_available = false;
	return 0;
}

/* EOF */
