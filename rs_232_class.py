#!/usr/bin/env python3

'''
James Fant-Male
University of Bath
December 2023
'''

import serial
from time import sleep

class rs_232_ctl:
	"""Provides control of CYP EL-21PIP HDMI switch viw RS-232 connection.
	"""
	def __init__(self, verbose=True, device='/dev/ttyUSB0'):
		"""Init serial connection to switcher device
		"""
		self.verbose = verbose
		self.ser = serial.Serial(device, baudrate=19200, timeout=1)
	
	def close(self):
		"""Flush and close serial connection.
		"""
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.close()
	
	def response_listen(self, display=True):
		"""Read serial data while available.
		"""
		data = []
		while True:
			newLine=self.ser.readline()
			if len(newLine) > 0:
				if display:
					print(newLine.decode('utf-8'))
				data.append(newLine.decode('utf-8'))
			else:
				break
		return data
	
	def vertical_flip(self, screen, enabled=False):
		"""Set vertical flip for screen to true or false
		"""
		response = 0
		if screen in [1, 2]:
			if enabled:
				self.ser.write(f'SET IN {screen} UP-SIDE DOWN ON\r'.encode('utf-8'))
			else:
				self.ser.write(f'SET IN {screen} UP-SIDE DOWN OFF\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid screen id, enter 1 or 2")
			response = 1
		return response
	
	def horizontal_flip(self, screen, enabled=False):
		"""Set horizotal flip for screen to true or false
		"""
		response = 0
		if screen in [1, 2]:
			if enabled:
				self.ser.write(f'SET IN {screen} FLIP ON\r'.encode('utf-8'))
			else:
				self.ser.write(f'SET IN {screen} FLIP OFF\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid screen id, enter 1 or 2")
			response = 1
		return response
		
	def set_window_layout(self, mode):
		"""Set window layout mode.
		
			mode [int]:
			1: Picture in Picture
			2: Side by Side
			4: Picture outside Picture
			5: Full screen
		"""
		response = 0
		if mode in [1, 2, 4, 5]:
			self.ser.write(f'SET WINDOW LAYOUT MODE {mode}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid layout mode, enter 1,2,4,5")
			response = 1
		return response
	
	def set_window_priority(self, source):
		"""Set which window will have top priority.
		"""
		response = 0
		if source in [1, 2]:
			self.ser.write(f'SET OUT A WINDOW PRIORITY {source}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid source id, enter 1 or 2")
			response = 1
		return response
	
	def set_window_swap(self, enabled):
		"""Swap windows in current layout.
		"""
		response = 0
		if int(enabled) in [0, 1]:
			self.ser.write(f'SET WINDOW SWAP {int(enabled)}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid enabled value, enter 0 or 1")
			response = 1
		return response
	
	def set_audio_source(self, source):
		"""Set which audio source to use
		"""
		response = 0
		if source in [1, 2]:
			self.ser.write(f'SET OUT A AUDIO SOURCE {source}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid source id, enter 1 or 2")
			response = 1
		return response
	
	def mute(self, enabled):
		"""Mute audio.
		"""
		response = 0
		if int(enabled) in [0, 1]:
			self.ser.write(f'SET OUT A MUTE {int(enabled)}\r'.encode('utf-8'))
			response = self.response_listen()
		else:
			print("Invalid enabled value, enter 0 or 1")
			response = 1
		return response
	
	def get_resolution(self):
		"""Get resolution of screen.
		"""
		response = 0
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.write(f'GET OUT A TIMING\r'.encode('utf-8'))
		serdata = self.response_listen()
		response = int(serdata[-1].split(' ')[-1].strip())
		if response == 0:
			resolution = ["native", None, None]
		elif response == 4:
			resolution = ["480P60", 640, 480]
		elif response == 6:
			resolution = ["720P60", 1280, 720]
		elif response == 10:
			resolution = ["1080P60", 1920, 1080]
		elif response == 11:
			resolution = ["576P50", 720, 576]
		elif response == 12:
			resolution = ["720P50", 1280, 720]
		elif response == 16:
			resolution = ["1080P24", 1920, 1080]
		elif response == 17:
			resolution = ["1080P25", 1920, 1080]
		elif response == 19:
			resolution = ["1080P30", 1920, 1080]
		elif response == 416:
			resolution = ["1024x768", 1024, 768]
		elif response == 417:
			resolution = ["1280x800", 1280, 800]
		elif response == 419:
			resolution = ["1280x1024", 1280, 1024]
		elif response == 420:
			resolution = ["1366x768", 1366, 768]
		elif response == 423:
			resolution = ["1440x900", 1440, 900]
		elif response == 424:
			resolution = ["1600x900RB", 1600, 900]
		elif response == 425:
			resolution = ["1600x1200", 1600, 1200]
		elif response == 426:
			resolution = ["1680x1050", 1680, 1050]
		elif response == 430:
			resolution = ["1920x1200RB", 1920, 1200]
		else:
			resolution = ["unknown", None, None]
			
		return resolution
		
	def set_vposition(self, screen, position):
		"""Set vertical position of screen. Position is in pixels, 0-(resolution-1).
		"""
		response = 0
		if screen in [1, 2]:
			self.ser.write(f'SET IN {screen} VPOSITION {position}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response
	
	def set_hposition(self, screen, position):
		"""Set horizontal position of screen. Position is in pixels, 0-(resolution-1).
		"""
		response = 0
		if screen in [1, 2]:
			self.ser.write(f'SET IN {screen} HPOSITION {position}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response
	
	def set_width(self, screen, width):
		"""Set width of screen. Width in pixels 0-resolution.
		"""
		response = 0
		if screen in [1, 2]:
			if width >= 0:
				self.ser.write(f'SET IN {screen} WIDTH {width}\r'.encode('utf-8'))
				if self.verbose:
					response = self.response_listen()
			else:
				print("Invalid width value, must be >= 0")
				response = 1
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response
	
	def set_height(self, screen, height):
		"""Set height of screeen. Height in pixels 0-resolution.
		"""
		response = 0
		if screen in [1, 2]:
			if height >= 0:
				self.ser.write(f'SET IN {screen} HEIGHT {height}\r'.encode('utf-8'))
				if self.verbose:
					response = self.response_listen()
			else:
				print("Invalid height value, must be >= 0")
				response = 1
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response
	
	def set_backdrop_colour(self, screen, colour):
		"""Set background colour for screen. Colour is "BLACK" or "BLUE".
		"""
		response = 0
		if screen in [1, 2]:
			if colour in ["BLACK", "BLUE"]:
				self.ser.write(f'SET IN {screen} BACKDROP Color {colour}\r'.encode('utf-8'))
				if self.verbose:
					response = self.response_listen()
			else:
				print("Invalid colour value, must be 'BLACK' or 'BLUE' ")
				response = 1
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response

	def set_still_image(self, screen, enabled=False):
		"""Enable/disable image freeze of screen.
		"""
		response = 0
		if screen in [1, 2]:
			if enabled:
				self.ser.write(f'SET IN {screen} IMAGE STILL ON\r'.encode('utf-8'))
			else:
				self.ser.write(f'SET IN {screen} IMAGE STILL OFF\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid screen id, enter 1 or 2")
			response = 1
		return response

	def set_display_text(self, text):
		"""Display OSD text. Text has max 32 characters.
		"""
		response = 0
		if len(text) < 33:
			self.ser.write(f'SET OUT A OSD TEXT {text}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Input too long, max 32 characters")
			response = 1
		return response

	def reset(self):
		"""Reset all settings to factory default.
		"""
		response = 0
		self.ser.write(b'SET FACTORY DEFAULT\r')
		print("Resetting, please wait...")
		sleep(10)
		if self.verbose:
			response = self.response_listen()
		return response

	def set_colour_format(self, screen, colFormat):
		"""Set colour format used for screen.
		
			colFormat [int]:
			1: RGB
			2: YPbPr 4:2:2
			3: YPbPr 4:4:4
		"""
		response = 0
		if screen in [1, 2]:
			if colFormat in [1, 2, 3]:
				self.ser.write(f'SET IN {screen} FORMAT {colFormat}\r'.encode('utf-8'))
				if self.verbose:
					response = self.response_listen()
			else:
				print("Invalid format value, must be 1-3 ")
				response = 1
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response

	def get_edid_info(self, screen):
		"""Get the EDID source currently used on screen.
		"""
		response = 0
		self.ser.flushInput()
		self.ser.flushOutput()
		if screen in [1, 2]:
			self.ser.write(f'GET IN {screen} EDID\r'.encode('utf-8'))
			response = self.response_listen()
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response
