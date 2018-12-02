import json
import os
import subprocess
import time
from datetime import datetime
from .name_generator import names
from .utils import record_mp3
from . import constants

class Recorder:
	def __init__(self, flusher):
		self._set_not_recording()
		self.flusher = flusher

	def _set_not_recording(self):
		self.is_recording = False
		self.funny_name = None
		self.filename = None
		self.filepath = None

	def toggle(self):
		if not self.is_recording:
			self.start_recording()
		else:
			self.stop_recording()

	def start_recording(self):
		if self.is_recording:
			raise constants.ValidationError("Already recording!")

		timestamp = datetime.today().strftime("%m-%d %I:%M%p")

		self.is_recording = True
		self.funny_name = names.generate()
		self.filename = timestamp + " " + self.funny_name + ".mp3"
		self.filepath = os.path.join(constants.RECORDING_DIRECTORY, self.filename)

		record_mp3.start(self.filepath)

	def stop_recording(self):
		if not self.is_recording:
			raise constants.ValidationError("Already recording!")

		record_mp3.interrupt()
		self.flusher.upload_and_delete_nonblocking(self.filepath)
		self._set_not_recording()
