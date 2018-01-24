/**
 * @file     main.c
 * @version  V0.1
 * @date     JAN 2018
 * @author   Kelve T. Henrique
 *
 * @mainpage XMC4500 + LIS3DH COMMUNICATION

 * @brief Establishing the communication between LIS3DH sensor and Computer using the XMC4500 as intermediator that filters and set thresholders\n
 *        on the raw data of sensor.

 * @section Usage

 * This project can be built from the command line,
 * using a Makefile. The latter provides the following commands:

 * @verbatim
 * make                        # builds the project
 * make debug                  # builds the project, start the debugger and print outputs into the './doc' directory
 * make flash                  # flash the application
 * make doc                    # generate this documentation
 * make clean                  # remove intermediate files
 * @endverbatim

 * @section Folders

 * The code is organized in various folders - checkout the comments below:

 * @verbatim
 * Makefile          # top level Makefile used for the command-line variant
 * doxygen           # doxygen configuration file
 * inc/              # header files
 * src/              # source files
 * bin/              # output folder - here you will find listings and binaries
 * doc/              # generated documentation as well as some relevant prints and the linearity analysis
 * system/           # CMSIS library, Infineon header files, linker script, etc.
 * xmclib/           # XMC library
 * @endverbatim
 *
 * @section Hardware
 * 
 * Some references to better understand the code and configure the HW
 * \image html doc/config.png "caption"
 *
 * @verbatim
 * GPIO toggle example flashes the leds of the board with a periodic rate.
 * LED1 is connected to P1.1
 * LED2 is connected to P1.0
 *
 * UART communication via USB-to-Serial cable
 * UART_TX P1_5 -> CABLE_RX
 * UART_RX P1_4 -> CABLE_TX
 *
 * I2C communication with the LIS3DH Accelerometer Sensor
 * LIS3DH_Vin               VDD3
 * LIS3DH_GND               GND
 * LIS3DH_SDA_PIN 			P0_5
 * LIS3DH_SCL_PIN 			P0_11
 * @endverbatim
 *
**/

#include <xmc4500_uart_lib.h>
#include <xmc4500_i2c_lib.h>
#include <xmc4500_interface_lib.h>

#include <lis3dh_driver.h>
#include <lis3dh_lib.h>

#define TICKS_PER_SECOND 1000
#define TICKS_WAIT 500

void SysTick_Handler (void)
{
    static uint32_t ticks = 0;
    static int32_t cnt = 0;

    check_button();

    ticks++;
    if (ticks == TICKS_WAIT) {
        XMC_GPIO_ToggleOutput (LED1);
        XMC_GPIO_ToggleOutput (LED2);

        cnt++;
        ticks = 0;
    }
}


int main (void){
    uint8_t button_pressed;
    uint8_t response;
    AxesRaw_t data;

    /* I2C CONFIGURATION */
    init_i2c();

    /* LEDs AND BUTTONS CONFIGURATION */
    init_interface();

    /* UART0 CHANNEL 0 CONFIGURATION */
    _init_uart0_ch0();

    /* SYSTEM TIMER CONFIGURATION */
    SysTick_Config (SystemCoreClock / TICKS_PER_SECOND);

    /* LIS3DH CONFIGURATION */
    response = init_lis3dh(LIS3DH_ODR_100Hz, LIS3DH_NORMAL, LIS3DH_FULLSCALE_2);
    if(response == 0){
        _uart_printf("SET ODR: OK\n");
        _uart_printf("SET MODE: OK\n");
        _uart_printf("SET FULLSCALE: OK\n");
        _uart_printf("SET AXIS: OK\n");
    }else 
        _uart_printf("ERROR: init_lis3dh\n");


    while(1){
        // Reading buttons
        if(read_buff(&button_pressed)){
            switch(button_pressed){
                case 1: // button_1 was pressed
                    _uart_printf("1");
                    break;
                case 2: // button_2 was pressed
                    _uart_printf("2");
                    break;
                default:
                    break;
            }
        } 

        //get Acceleration Raw data  
        response = LIS3DH_GetAccAxesRaw(&data);
        if(response==1){
            //print data values
            if(data.AXIS_X >  2000) _uart_send_char('r');
            if(data.AXIS_X >  6000) _uart_send_char('R');
            if(data.AXIS_X < -2000) _uart_send_char('l');
            if(data.AXIS_X < -6000) _uart_send_char('L');
            if(data.AXIS_Y >  2000) _uart_send_char('u');
            if(data.AXIS_Y >  6000) _uart_send_char('U');
            if(data.AXIS_Y < -2000) _uart_send_char('d');
            if(data.AXIS_Y < -6000) _uart_send_char('D');
          ///  if(data.AXIS_Z >  2000) _uart_send_char('T');
          ///  if(data.AXIS_Z < -2000) _uart_send_char('B');

//            _uart_printf("X=%6d Y=%6d Z=%6d \r\n", data.AXIS_X, data.AXIS_Y, data.AXIS_Z);
        }
        else _uart_send_char('E');

    }
}

/* EOF */
