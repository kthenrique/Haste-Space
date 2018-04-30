/**
 * @file     lis3dh_lib.h
 * @version  V0.1
 * @date     Nov 2017
 * @author   Kelve T. Henrique
 *
 * @brief                                                         
 *                                   
 */


#ifndef INC_LIS3DH_LIB_H_
#define INC_LIS3DH_LIB_H_

#include <lis3dh_driver.h>
#include <stdint.h>

uint8_t init_lis3dh(LIS3DH_ODR_t odr, LIS3DH_Mode_t powermode, LIS3DH_Fullscale_t fullscale);
uint8_t config_6d(uint8_t threshold);
uint8_t config_freefall(void);

#endif /* INC_LIS3DH_LIB_H_ */
