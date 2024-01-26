#!/usr/bin/env python3

'''
Functional test script for rs-232 control of HDMI switcher.

James Fant-Male
University of Bath
January 2024
'''

import time
from rs_232_class import rs_232_ctl

rs232_controller = rs_232_ctl(verbose=True)

#rs232_controller.reset()
#time.sleep(3)

print("Setup PIP Mode")
resolution = rs232_controller.get_resolution()
print(resolution)

scale = 50
width = 16*scale
height = 9*scale
print(width, height)
#rs232_controller.set_window_layout(1)
#rs232_controller.set_hposition(2, resolution[1]-width)
#rs232_controller.set_vposition(2, resolution[2]-height)
#rs232_controller.set_height(2, height)
#rs232_controller.set_width(2, width)

rs232_controller.set_window_layout(5)
rs232_controller.set_window_priority(1)
rs232_controller.set_window_swap(False)
rs232_controller.save_preset(3)

time.sleep(5)

rs232_controller.set_window_swap(True)
rs232_controller.set_window_priority(2)
time.sleep(5)
rs232_controller.recall_preset(3)
rs232_controller.close()

