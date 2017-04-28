#!/usr/bin/env python2

from __future__ import unicode_literals #for py3 strings
from skidl import *

#signals
#power
gnd = Net('GND')
vin = Net('+5V')
vled = Net('VLED')
#PWMs
led1_ctrl = Net('CTRL1')
led2_ctrl = Net('CTRL2')
led3_ctrl = Net('CTRL3')
led4_ctrl = Net('CTRL4')
led5_ctrl = Net('CTRL5')
led6_ctrl = Net('CTRL6')
#I2C
sda = Net('SDA')
scl = Net('SCL')

parts = SchLib(tool=SKIDL).add_parts(*[
    Part(name=u'TK1_expansion_J3A2',dest=TEMPLATE,tool=SKIDL,keywords=u'NVIDIA JETSON TK1 EXPANSION J3A2',
        description=u'Nvidia Jetson TK1 Expansion Connector',ref_prefix='J',num_units=1,do_erc=True,footprint=u'generated:Jetson_TK1_Expansion_Connector_J3A2',
        pins=[Pin(num=str(p), name=('P'+str(p)), func=Pin.PASSIVE, do_erc=True) for p in range(1, (3*25+1))]),

    Part(name=u'TK1_expansion_J3A1',dest=TEMPLATE,tool=SKIDL,keywords=u'NVIDIA JETSON TK1 EXPANSION J3A1',
        description=u'Nvidia Jetson TK1 Expansion Connector',ref_prefix='J',num_units=1,do_erc=True,footprint=u'generated:Jetson_TK1_Expansion_Connector_J3A1',
        pins=[Pin(num=str(p), name=('P'+str(p)), func=Pin.PASSIVE, do_erc=True) for p in range(1, (2*25+1))])
    ])

#main connector (I2C, +5V supply)
main_connector = Part(parts, 'TK1_expansion_J3A2', footprint='generated:Jetson_TK1_Expansion_Connector_J3A2')
main_connector[1] += vin
main_connector[8] += sda
main_connector[11] += scl
main_connector[14] += gnd

#vled connector
vled_connector = Part('conn', 'CONN_01x02', footprint='Connectors:bornier2')
vled_connector[1] += vled
vled_connector[2] += gnd

#PCA9685 led driver
pwm_drv = Part('nxp', 'PCA9685PW', footprint='Housings_SSOP:TSSOP-28_4.4x9.7mm_Pitch0.65mm')
c_pwm_drv = Part('device', 'C', value='100n', footprint='Capacitors_SMD:C_0805')
gnd += pwm_drv[14], pwm_drv[23], c_pwm_drv[2]
vin += pwm_drv[28], c_pwm_drv[1]
pwm_drv[6] += led1_ctrl
pwm_drv[7] += led2_ctrl
pwm_drv[8] += led3_ctrl
pwm_drv[9] += led4_ctrl
pwm_drv[10] += led5_ctrl
pwm_drv[11] += led6_ctrl
pwm_drv[27] += sda
pwm_drv[26] += scl
#TODO: pin header for selecting i2c addr?

#add Power-LED subcircuits
from subcircuits import power_led_driver
power_led_driver(vin, gnd, vled, led1_ctrl, '1K')
power_led_driver(vin, gnd, vled, led2_ctrl, '1K')
power_led_driver(vin, gnd, vled, led3_ctrl, '1K')
power_led_driver(vin, gnd, vled, led4_ctrl, '1K')
power_led_driver(vin, gnd, vled, led5_ctrl, '1K')
power_led_driver(vin, gnd, vled, led6_ctrl, '1K')

generate_netlist()
