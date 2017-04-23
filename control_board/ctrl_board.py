#!/usr/bin/env python2

from __future__ import unicode_literals #for py3 strings
from skidl import *

#internal lib
lights_lib = SchLib(tool=SKIDL).add_parts(*[
    Part(name='MBI1801',dest=TEMPLATE,tool=SKIDL,keywords=u'POWER LED DRIVER MBI1801',description=u'All-Ways-On High-Power LED Driver',ref_prefix='U',num_units=1,do_erc=True,footprint=u'TO_SOT_Packages_SMD:TO-263-5Lead',pins=[
        Pin(num='1',name='~OE',do_erc=True),
        Pin(num='2',name='VDD',func=Pin.PWRIN,do_erc=True),
        Pin(num='3',name='GND',func=Pin.PWRIN,do_erc=True),
        Pin(num='4',name='Rext',func=Pin.PWROUT,do_erc=True),
        Pin(num='5',name='~OUT',func=Pin.OUTPUT,do_erc=True)])])

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

#main connector (I2C, +5V supply)
main_connector = Part('conn', 'CONN_02x03', footprint='generated:SMD_Female_Pin_Header_2x03_2mm')
main_connector[1] += sda
main_connector[2] += scl
main_connector[3] += gnd
main_connector[4] += vin

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
def led_controller(vin, gnd, vled, ctrl_in, rext_val):
    led_drv = Part(lights_lib, 'MBI1801')
    out_conn = Part('conn', 'CONN_01x04', footprint='Connectors_wb:THT_4P')
    rext = Part('device', 'R', value=rext_val, footprint='Resistors_SMD:R_0805')
    c_vin = Part('device', 'C', value='100n', footprint='Capacitors_SMD:C_0805')
    c2 = Part('device', 'C', value='100n', footprint='Capacitors_THT:CP_Radial_D4.0mm_P2.00mm')
    gnd += c_vin[2], rext[2], led_drv[3], c2[2]
    vin += led_drv[2], c_vin[1]
    vled += c2[1], out_conn[3], out_conn[4]
    led_drv[1] += ctrl_in
    led_drv[5] += out_conn[1], out_conn[2]
    led_drv[4] += rext[1]

led_controller(vin, gnd, vled, led1_ctrl, '1K')
led_controller(vin, gnd, vled, led2_ctrl, '1K')
led_controller(vin, gnd, vled, led3_ctrl, '1K')
led_controller(vin, gnd, vled, led4_ctrl, '1K')

generate_netlist()
