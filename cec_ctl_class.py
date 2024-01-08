#!/usr/bin/env python3
import sys
import os
import subprocess
print(sys.version)

class cec_ctl:
	def __init__(self, verbose=False):
		self.verbose = verbose
		try:
			if self.verbose:
				subprocess.run(['sudo', 'cec-ctl', '-d/dev/cec0', '--playback', '-S'], check=True)
			else:
				subprocess.run(['sudo', 'cec-ctl', '-d/dev/cec0', '--playback', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
				
	def power_on(self):
		try:
			if self.verbose:
				subprocess.run(['sudo', 'cec-ctl', '-d/dev/cec0', '--to', '0', '--image-view-on', '-S'], check=True)
			else:
				subprocess.run(['sudo', 'cec-ctl', '-d/dev/cec0', '--to', '0', '--image-view-on', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
			
	def standby(self):
		try:
			if self.verbose:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--standby', '-S'], check=True)
			else:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--standby', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
	
	def mute(self):
		try:
			if self.verbose:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=mute', '-S'], check=True)
			else:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=mute', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
			
	def volume_up(self):
		try:
			if self.verbose:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=volume-up', '-S'], check=True)
			else:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=volume-up', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
	
	def volume_down(self):
		try:
			if self.verbose:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=volume-down', '-S'], check=True)
			else:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=volume-down', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
			
	def channel_up(self):
		try:
			if self.verbose:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=channel-up', '-S'], check=True)
			else:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=channel-up', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
			
	def channel_down(self):
		try:
			if self.verbose:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=channel-down', '-S'], check=True)
			else:
				subprocess.run(['cec-ctl', '-d/dev/cec0', '--to', '0', '--user-control-pressed', 'ui-cmd=channel-down', '-s'], check=True)
		except subprocess.CalledProcessError as e:
			print(e)
