/**
 * @file     xmc4500_i2c_lib.c
 * @version  V0.1
 * @date     Nov 2017
 * @author   Kelve T. Henrique
 *
 * @brief                                                         
 *                                   
 */

#include <xmc4500_i2c_lib.h>

/**
 * @brief  Initialisation of I2C Module of XMC4500
 *         
 */
void init_i2c(void){
    /* CONFIGURING THE I2C MODULE OF XMC4500 */

    XMC_GPIO_CONFIG_t i2c_sda = {                   // Configures the SDA
        .mode = XMC_GPIO_MODE_OUTPUT_OPEN_DRAIN_ALT2,
        .output_strength = XMC_GPIO_OUTPUT_STRENGTH_MEDIUM
    };

    XMC_GPIO_CONFIG_t i2c_scl = {                   // Configures the SCL
        .mode = XMC_GPIO_MODE_OUTPUT_OPEN_DRAIN_ALT2,
        .output_strength = XMC_GPIO_OUTPUT_STRENGTH_MEDIUM
    };

    XMC_I2C_CH_CONFIG_t i2c_cfg = {                // Configures the Baudrate
        .baudrate = 100000U,
    };

    XMC_I2C_CH_Init (XMC_I2C1_CH0, &i2c_cfg);

    XMC_I2C_CH_SetInputSource (XMC_I2C1_CH0, XMC_I2C_CH_INPUT_SDA, USIC1_C0_DX0_P0_5);
    XMC_I2C_CH_SetInputSource (XMC_I2C1_CH0, XMC_I2C_CH_INPUT_SCL, USIC1_C0_DX1_SCLKOUT);

    XMC_I2C_CH_Start (XMC_I2C1_CH0);

    XMC_GPIO_Init (LIS3DH_SCL_PIN, &i2c_scl); // configures the chosen pin as SCL
    XMC_GPIO_Init (LIS3DH_SDA_PIN, &i2c_sda); // configures the chosen pin as SDA

    /* FINISHED CONFIGURING THE I2C MODULE OF XMC4500 */
}
