from __future__ import unicode_literals
from skidl import *

#MBI1801 Power-LED driver + elements
@SubCircuit
def power_led_driver(vin, gnd, vled, ctrl_in, rext_val):
    lights_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(name='MBI1801',dest=TEMPLATE,tool=SKIDL,keywords=u'POWER LED DRIVER MBI1801',description=u'All-Ways-On High-Power LED Driver',ref_prefix='U',num_units=1,do_erc=True,footprint=u'TO_SOT_Packages_SMD:TO-263-5Lead',pins=[
            Pin(num='1',name='~OE',do_erc=True),
            Pin(num='2',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='3',name='GND',func=Pin.PWRIN,do_erc=True),
            Pin(num='4',name='Rext',func=Pin.PWROUT,do_erc=True),
            Pin(num='5',name='~OUT',func=Pin.OUTPUT,do_erc=True)])])

    led_drv = Part(lights_lib, 'MBI1801')
    out_conn = Part('conn', 'CONN_01x04', footprint='generated:MicroMatch_4p')
    rext = Part('device', 'R', value=rext_val, footprint='Resistors_SMD:R_0805')
    c_vin = Part('device', 'C', value='100n', footprint='Capacitors_SMD:C_0805')
    c2 = Part('device', 'C', value='100n', footprint='Capacitors_THT:CP_Radial_D4.0mm_P2.00mm')
    gnd += c_vin[2], rext[2], led_drv[3], c2[2]
    vin += led_drv[2], c_vin[1]
    vled += c2[1], out_conn[3], out_conn[4]
    led_drv[1] += ctrl_in
    led_drv[5] += out_conn[1], out_conn[2]
    led_drv[4] += rext[1]
