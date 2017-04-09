#!/usr/bin/env python2

from __future__ import unicode_literals #for py3 strings
from skidl import *

lib_search_paths[KICAD].append('lib')

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
#I2C
sda = Net('SDA')
scl = Net('SCL')

#LED connector
leds_out_conn = Part('conn', 'CONN_01X08', footprint='Connectors:IDC_Header_Straight_8pins')

#TODO: i2c, vin connector
#main_connector = Part('conn', 'CONN_01x04', footprint='')

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
pwm_drv[27] += sda
pwm_drv[26] += scl
#TODO: pin header for selecting i2c addr?

#MBI1801 led driver + elements
@SubCircuit
def led_ctrl(ctrl_in, anode, cathode, rext_val):
    global gnd
    global vin
    global vled
    led_drv = Part('macroblock', 'MBI1801', footprint='TO_SOT_Packages_SMD:TO-263-5Lead')
    rext = Part('device', 'R', value=rext_val, footprint='Resistors_SMD:R_0805')
    c_vin = Part('device', 'C', value='100n', footprint='Capacitors_SMD:C_0805')
    c2 = Part('device', 'C', value='100n', footprint='Capacitors_THT:CP_Radial_D4.0mm_P2.00mm')
    gnd += c_vin[2], rext[2], led_drv[3], c2[2]
    vin += led_drv[2], c_vin[1]
    vled += c2[1], anode
    led_drv[1] += ctrl_in
    led_drv[5] += cathode
    led_drv[4] += rext[1]

led_ctrl(led1_ctrl, leds_out_conn[1], leds_out_conn[2], '1K')
led_ctrl(led2_ctrl, leds_out_conn[3], leds_out_conn[4], '1K')
led_ctrl(led3_ctrl, leds_out_conn[5], leds_out_conn[6], '1K')
led_ctrl(led3_ctrl, leds_out_conn[7], leds_out_conn[8], '1K')

ERC()
generate_netlist()
