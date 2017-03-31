#!/usr/bin/env python2

from skidl import *

gnd = Net('GND')
vin = Net('+5V')
pwm_driver = Part('nxp', 'PCA9685PW', footprint='Housings_SSOP:TSSOP-28_4.4x9.7mm_Pitch0.65mm')

generate_netlist()
