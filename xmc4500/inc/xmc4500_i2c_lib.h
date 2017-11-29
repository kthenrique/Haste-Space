/**
 * @file     xmc4500_i2c_lib.h
 * @version  V0.1
 * @date     Nov 2017
 * @author   Kelve T. Henrique
 *
 * @brief                                                         
 *                                   
 */

#ifndef INC_XMC4500_I2C_LIB_H_
#define INC_XMC4500_I2C_LIB_H_

#include <xmc_gpio.h>
#include <xmc_i2c.h>

//#include <xmc_usic.h>

#define LIS3DH_SDA_PIN 			P0_5     // pins to be used as I2C channels       
#define LIS3DH_SCL_PIN 			P0_11    // pins to be used as I2C channels

void init_i2c(void);

#endif /* INC_XMC4500_I2C_LIB_H_ */
