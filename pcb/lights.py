#!/usr/bin/env python2

import sys
sys.path.append('../../skidl/skidl')

from skidl import *

lib_search_paths_kicad.append('lib')

gnd = Net('GND')
vin = Net('+5V')
pwm_driver = Part('nxp', 'PCA9685PW', footprint='Housings_SSOP:TSSOP-28_4.4x9.7mm_Pitch0.65mm')
led_drv = Part('macroblock', 'MBI1801', footprint='TODO')

generate_netlist()
