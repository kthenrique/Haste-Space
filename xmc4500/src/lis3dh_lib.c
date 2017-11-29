/**
 * @file     lis2dh_lib.c
 * @version  V0.1
 * @date     Nov 2017
 * @author   Kelve T. Henrique
 *
 * @brief                                                         
 *                                   
 */

#include <lis3dh_lib.h>

uint8_t init_lis3dh(LIS3DH_ODR_t odr, LIS3DH_Mode_t powermode, LIS3DH_Fullscale_t fullscale){
    uint8_t response;

    //Inizialize MEMS Sensor
    //set ODR (turn ON device)
    response = LIS3DH_SetODR(odr);
    if(response!=1){
        return 1;
    }
    //set PowerMode 
    response = LIS3DH_SetMode(powermode);
    if(response!=1){
        return 1;
    }
    //set Fullscale
    response = LIS3DH_SetFullScale(fullscale);
    if(response!=1){
        return 1;
    }
    //set axis Enable
    response = LIS3DH_SetAxis(LIS3DH_X_ENABLE | LIS3DH_Y_ENABLE | LIS3DH_Z_ENABLE);
    if(response!=1){
        return 1;
    }
    return 0;
}

uint8_t config_6d(uint8_t threshold){
    uint8_t response;

    //configure Mems Sensor
    //set Interrupt Threshold 
    response = LIS3DH_SetInt1Threshold(threshold);
    if(response!=1){
        return 1;
    }
    //set Interrupt configuration (all enabled)
    response = LIS3DH_SetIntConfiguration(LIS3DH_INT1_ZHIE_ENABLE | LIS3DH_INT1_ZLIE_ENABLE |
            LIS3DH_INT1_YHIE_ENABLE | LIS3DH_INT1_YLIE_ENABLE |
            LIS3DH_INT1_XHIE_ENABLE | LIS3DH_INT1_XLIE_ENABLE ); 
    if(response!=1){
        return 1;
    }
    //set Interrupt Mode
    response = LIS3DH_SetIntMode(LIS3DH_INT_MODE_6D_POSITION);
    if(response!=1){
        return 1;
    }

    return 0;
}

uint8_t config_freefall(void){
    uint8_t response;

    LIS3DH_WriteReg(LIS3DH_CTRL_REG1, 0xA7);
    LIS3DH_WriteReg(LIS3DH_CTRL_REG2, 0x00);
    LIS3DH_WriteReg(LIS3DH_CTRL_REG3, 0x40);
    LIS3DH_WriteReg(LIS3DH_CTRL_REG4, 0x00);
    LIS3DH_WriteReg(LIS3DH_CTRL_REG5, 0x08);
    LIS3DH_WriteReg(LIS3DH_INT1_THS,  0x16);
    LIS3DH_WriteReg(LIS3DH_INT1_DURATION, 0x03);
    LIS3DH_WriteReg(LIS3DH_INT1_CFG,  0x95);
//    
//    // High-pass filter disabled
//    response = LIS3DH_HPFAOI1Enable(MEMS_DISABLE);
//    if(response != 1){
//        return 1;
//    }
//
//    // Interrupt driven to INT1 pad
//    response = LIS3DH_SetInt1Pin(0x40);
//    if(response != 1){
//        return 1;
//    }
//
//    // FS = 2g
//    response = LIS3DH_SetFullScale(LIS3DH_FULLSCALE_2);
//    if(response != 1){
//        return 1;
//    }
//
//    // Interrupt latched
//    response = LIS3DH_Int1LatchEnable(MEMS_ENABLE);
//    if(response != 1){
//        return 1;
//    }
//
//    // Set free-fall threshold = 350mg
//    response = LIS3DH_SetInt1Threshold(0x16);
//    if(response != 1){
//        return 1;
//    }
//
//    // Set minimum event duration - 30 msec
//    response = LIS3DH_SetInt1Duration(0x1);
//    if(response != 1){
//        return 1;
//    }
//
//    // Configure free-fall recognition
//    response = LIS3DH_SetIntConfiguration(0x95);
//    if(response != 1){
//        return 1;
//    }
    
    return 0;
}
