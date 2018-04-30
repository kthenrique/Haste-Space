/**
 * @file     xmc4500_interface_lib.h
 * @version  V0.1
 * @date     Nov 2017
 * @author   Kelve T. Henrique
 *
 * @brief                                                         
 *                                   
 */

#ifndef INC_XMC4500_INTERFACE_LIB_H_
#define INC_XMC4500_INTERFACE_LIB_H_

#include <XMC4500.h>
#include <xmc_gpio.h>

#define BUFF_SIZE 7
#define LED1 P1_1
#define LED2 P1_0

#define CHECK_BUTTON(button) ((button) == 1 ? (RD_REG(PORT1->IN, \
                                               PORT1_IN_P14_Msk, \
                                               PORT1_IN_P14_Pos)) :\
                                              (RD_REG(PORT1->IN, \
                                               PORT1_IN_P15_Msk, \
                                                PORT1_IN_P15_Pos)))

void init_interface(void);
void init_buff(void);
void write_buff(uint8_t new);
uint8_t read_buff(uint8_t *old);
void check_button(void);

#endif /* INC_XMC4500_INTERFACE_LIB_H_ */
