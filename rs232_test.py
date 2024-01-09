#!/usr/bin/env python3

'''
Functional test script for rs-232 control of HDMI switcher.

James Fant-Male
University of Bath
December 2023
'''

import time
from rs_232_class import rs_232_ctl

rs232_controller = rs_232_ctl(verbose=False)

##Test modes
testAll = True
vFlip = False
hFlip = False
layout = False  
priority = False
swap = False
audio = False
screen_position = False
backdrop_colour = False
imageStill = False
displayText = False
colFormat = False

if testAll:
	print("Testing ALL parameters. Duration Approx 3min.")

## Reset factory default
print(rs232_controller.reset())
time.sleep(3)

print(rs232_controller.get_edid_info(1))

## Layout Testing
if layout or testAll:
	print("PIP Mode")
	print(rs232_controller.set_window_layout(1))
	time.sleep(2)
	print("SBS Mode")
	print(rs232_controller.set_window_layout(2))
	time.sleep(2)
	print("Unknown Mode")
	print(rs232_controller.set_window_layout(3))
	time.sleep(2)
	print("POP Mode")
	print(rs232_controller.set_window_layout(4))
	time.sleep(2)
	print("Full Screen Mode")
	print(rs232_controller.set_window_layout(5))
	time.sleep(2)
	print("Error test")
	print(rs232_controller.set_window_layout(6))
	time.sleep(2)

## Upside Down Testing
if vFlip or testAll:
	rs232_controller.set_window_layout(2)
	time.sleep(1)
	print("Display 1 Upside Down ON")
	print(rs232_controller.vertical_flip(1, enabled=True))
	time.sleep(2)
	print("Display 1 Upside Down OFF")
	print(rs232_controller.vertical_flip(1, enabled=False))
	time.sleep(2)
	print("Display 2 Upside Down ON")
	print(rs232_controller.vertical_flip(2, enabled=True))
	time.sleep(2)
	print("Display 2 Upside Down OFF")
	print(rs232_controller.vertical_flip(2, enabled=False))
	time.sleep(2)
	print("Display Upside Down Error check")
	print(rs232_controller.vertical_flip(3, enabled=False))
	time.sleep(2)

## Horizontal flip Testing
if hFlip or testAll:
	rs232_controller.set_window_layout(2)
	time.sleep(1)
	print("Display 1 Upside Down ON")
	print(rs232_controller.horizontal_flip(1, enabled=True))
	time.sleep(2)
	print("Display 1 Upside Down OFF")
	print(rs232_controller.horizontal_flip(1, enabled=False))
	time.sleep(2)
	print("Display 2 Upside Down ON")
	print(rs232_controller.horizontal_flip(2, enabled=True))
	time.sleep(2)
	print("Display 2 Upside Down OFF")
	print(rs232_controller.horizontal_flip(2, enabled=False))
	time.sleep(2)
	print("Display Upside Down Error check")
	print(rs232_controller.horizontal_flip(3, enabled=False))
	time.sleep(2)

## Screen Priority Testing
if priority or testAll:
	rs232_controller.set_window_layout(1)
	time.sleep(1)
	print("Input 2")
	print(rs232_controller.set_window_priority(2))
	time.sleep(2)
	print("Input 1")
	print(rs232_controller.set_window_priority(1))
	time.sleep(2)
	print("Error test")
	print(rs232_controller.set_window_priority(3))
	time.sleep(2)

## Screen Swap Testing
if swap or testAll:
	rs232_controller.set_window_priority(2)
	rs232_controller.set_window_layout(1)
	time.sleep(1)
	print("Swap True")
	print(rs232_controller.set_window_swap(1))
	time.sleep(2)
	print("Swap False")
	print(rs232_controller.set_window_swap(0))
	time.sleep(2)
	print(rs232_controller.set_window_layout(2))
	time.sleep(2)
	print("Swap True")
	print(rs232_controller.set_window_swap(True))
	time.sleep(2)
	print("Swap False")
	print(rs232_controller.set_window_swap(False))
	time.sleep(2)
	print("Error Test")
	print(rs232_controller.set_window_swap(3))
	time.sleep(2)

## Audio function testing
if audio or testAll:
	print("Audio source 1")
	print(rs232_controller.set_audio_source(1))
	time.sleep(2)
	print("Audio source 2")
	print(rs232_controller.set_audio_source(2))
	time.sleep(2)
	print("Audio source error test")
	print(rs232_controller.set_audio_source(3))
	time.sleep(2)
	print("Mute On")
	print(rs232_controller.mute(1))
	time.sleep(2)
	print("Mute Off")
	print(rs232_controller.mute(False))
	time.sleep(2)
	print("Mute Error test")
	print(rs232_controller.mute(3))
	time.sleep(2)
	
## Screen position testing
if screen_position or testAll:
	rs232_controller.set_window_layout(1)
	rs232_controller.set_window_swap(False)
	rs232_controller.set_window_priority(2)
	rs232_controller.set_backdrop_colour(1, "BLUE")
	rs232_controller.set_backdrop_colour(2, "BLACK")
	time.sleep(1)
	print("Testing vertical position screen 2")
	for vposition in range(-400, 1000, 300):
		print(rs232_controller.set_vposition(2, vposition))
		time.sleep(0.3)
	
	print("Testing horizontal position screen 2")
	for hposition in range(-400, 1700, 300):
		print(rs232_controller.set_hposition(2, hposition))
		time.sleep(0.3)
	
	print("Testing width screen 2")
	for width in range(-200, 1000, 200):
		print(rs232_controller.set_width(2, width))
		time.sleep(0.3)
	
	print("Testing height screen 2")
	for height in range(-200, 1000, 200):
		print(rs232_controller.set_height(2, height))
		time.sleep(0.3)
	
	print("Testing width screen 1")
	for width in range(-200, 2300, 300):
		print(rs232_controller.set_width(1, width))
		time.sleep(0.3)
	
	print("Testing height screen 1")
	for height in range(-200, 1500, 300):
		print(rs232_controller.set_height(1, height))
		time.sleep(0.5)
	
	rs232_controller.set_window_swap(True)
	time.sleep(1)
	print("Testing vertical position screen 1")
	for vposition in range(-400, 1000, 300):
		print(rs232_controller.set_vposition(1, vposition))
		time.sleep(0.3)
	
	print("Testing horizontal position screen 1")
	for hposition in range(-400, 1700, 300):
		print(rs232_controller.set_hposition(1, hposition))
		time.sleep(0.5)

	print("Testing width screen 1")
	for width in range(-200, 1000, 200):
		print(rs232_controller.set_width(1, width))
		time.sleep(0.3)
	
	print("Testing height screen 1")
	for height in range(-200, 1000, 200):
		print(rs232_controller.set_height(1, height))
		time.sleep(0.3)
	
	print("Testing width screen 2")
	for width in range(-200, 2300, 300):
		print(rs232_controller.set_width(2, width))
		time.sleep(0.3)
	
	print("Testing height screen 2")
	for height in range(-200, 1500, 300):
		print(rs232_controller.set_height(2, height))
		time.sleep(0.3)

## Change background colour testing
if backdrop_colour or testAll:
	rs232_controller.set_window_layout(1)
	rs232_controller.set_window_swap(False)
	time.sleep(1)
	print("Testing background colours")
	print(rs232_controller.set_backdrop_colour(1, "BLACK"))
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(1, 'BLUE'))
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(2, "BLACK"))
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(2, "BLUE"))
	time.sleep(1)
	print("Error test")
	print(rs232_controller.set_backdrop_colour(1, "blue"))
	time.sleep(1)
	rs232_controller.set_window_swap(True)
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(1, "BLACK"))
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(1, 'BLUE'))
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(2, "BLACK"))
	time.sleep(1)
	print(rs232_controller.set_backdrop_colour(2, "BLUE"))
	time.sleep(1)
	print("Error test")
	print(rs232_controller.set_backdrop_colour(1, "BLA"))

## Still image testing  
if imageStill or testAll:
	print("Display 1 image still ON")
	print(rs232_controller.set_still_image(1, enabled=True))
	time.sleep(5)
	print("Display 1 image still OFF")
	print(rs232_controller.set_still_image(1, enabled=False))
	time.sleep(2)
	print("Display 2 Uimage still ON")
	print(rs232_controller.set_still_image(2, enabled=True))
	time.sleep(5)
	print("Display 2 image still OFF")
	print(rs232_controller.set_still_image(2, enabled=False))
	time.sleep(2)
	print("Display image still Error check")
	print(rs232_controller.set_still_image(3, enabled=False))
	time.sleep(2)

## Display text testing
if displayText or testAll:
	rs232_controller.set_window_layout(1)
	rs232_controller.set_window_swap(False)
	rs232_controller.set_window_priority(2)
	print("Test text display")
	print(rs232_controller.set_display_text("TESTING TESTING TESTING TESTING"))
	time.sleep(10)
	print("Error test")
	print(rs232_controller.set_display_text("This string should be far far far far far too looooong"))

## Colour format testing
if colFormat:
	print("Test colour formats")
	print(rs232_controller.set_colour_format(1, 1))
	time.sleep(2)
	print(rs232_controller.set_colour_format(1, 2))
	time.sleep(2)
	print(rs232_controller.set_colour_format(1, 3))
	time.sleep(2)
	

## Reset to factory default
print(rs232_controller.reset())
time.sleep(3)

rs232_controller.close()

print("Testing Completed")
