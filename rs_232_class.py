import serial
from time import sleep

class rs_232_ctl:
	def __init__(self, verbose=True, device='/dev/ttyUSB0'):
		self.verbose = verbose
		self.ser = serial.Serial(device, baudrate=19200, timeout=1)
	
	def close(self):
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.close()
	
	def response_listen(self, display=False):
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
		response = 0
		if int(enabled) in [0, 1]:
			self.ser.write(f'SET OUT A MUTE {int(enabled)}\r'.encode('utf-8'))
			if self.verbose:
				response = self.response_listen()
		else:
			print("Invalid enabled value, enter 0 or 1")
			response = 1
		return response
	
	def set_vposition(self, screen, position):
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
		response = 0
		self.ser.write(b'SET FACTORY DEFAULT\r')
		print("Resetting, please wait...")
		sleep(10)
		if self.verbose:
			response = self.response_listen()
		return response

	def set_colour_format(self, screen, colFormat):
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
		response = 0
		if screen in [1, 2]:
			self.ser.write(f'GET IN {screen} EDID\r'.encode('utf-8'))
			response = self.response_listen()
		else:
			print("Invalid screen value, enter 1 or 2")
			response = 1
		return response
