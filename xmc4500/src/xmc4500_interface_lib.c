/**
 * @file     xmc4500_interface_lib.c
 * @version  V0.1
 * @date     Nov 2017
 * @author   Kelve T. Henrique
 *
 * @brief                                                         
 *                                   
 */

#include <xmc4500_interface_lib.h>

uint8_t button_1, button_2;
uint8_t in_buff, out_buff, full_buff, empty_buff;
uint8_t buff[BUFF_SIZE];


/**
 * @brief  Initialisation of I2C Module of XMC4500
 *         
 */
void init_interface(void){
    XMC_GPIO_CONFIG_t config;

    config.mode = XMC_GPIO_MODE_OUTPUT_PUSH_PULL;
    config.output_level = XMC_GPIO_OUTPUT_LEVEL_HIGH;
    config.output_strength = XMC_GPIO_OUTPUT_STRENGTH_MEDIUM;

    XMC_GPIO_Init (LED1, &config);

    config.output_level = XMC_GPIO_OUTPUT_LEVEL_LOW;
    XMC_GPIO_Init (LED2, &config);
   // INPUTS:
   //   1. configuration (Direct input(no devices))
    PORT1->IOCR12 &= ~PORT1_IOCR12_PC14_Msk; // BUTTON_1
    PORT1->IOCR12 &= ~PORT1_IOCR12_PC15_Msk; // BUTTON_2
   //   2. hardware control:
   //       no hw control to peripheral
   //   3. pin power save:
   //       not applicable


    init_buff();
   // Initialising variables:
    button_1 = 0;
    button_2 = 0;
}


/**
 * @brief  Initialisation of I2C Module of XMC4500
 *         
 */
void check_button(void){
    if (CHECK_BUTTON(1) == 0)
        button_1 = 1;
    if ((CHECK_BUTTON(1) == 1) && (button_1 == 1)){
        write_buff(1);
        button_1 = 0;
    }
    if (CHECK_BUTTON(2) == 0)
        button_2 = 1;
    if ((CHECK_BUTTON(2) == 1) && (button_2 == 1)){
        write_buff(2);
        button_2 = 0;
    }
}

/**
 * @brief  Initialisation of I2C Module of XMC4500
 *         
 */
void init_buff(void){

    in_buff = 0;
    out_buff = 0;
    full_buff = 0;
    empty_buff = 1;
}

/**
 * @brief  Initialisation of I2C Module of XMC4500
 *         
 */
void write_buff(uint8_t new){

    if(full_buff)
        return;

    in_buff = (in_buff + 1) % BUFF_SIZE;
    buff[in_buff] = new;
    if(in_buff == out_buff)
        full_buff = 1;
    
    empty_buff = 0;
    return;
}

/**
 * @brief  Initialisation of I2C Module of XMC4500
 *         
 */
uint8_t read_buff(uint8_t *old){

    if(empty_buff)
        return 0;

    out_buff = (out_buff + 1) % BUFF_SIZE;
    *old = buff[out_buff];
    if(in_buff == out_buff)
        empty_buff = 1;
        
    full_buff = 0;
    return 1;
}
