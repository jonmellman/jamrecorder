from datetime import datetime
import os
import threading
from .utils import dropbox

class Flusher:
	def __init__(self, uploader):
		self.uploader = uploader

	def upload_and_delete(self, filepath):
		self.uploader.upload(filepath)
		print("Deleting", filepath)
		os.remove(filepath)

	def upload_and_delete_nonblocking(self, filepath):
		thread = threading.Thread(target=self.upload_and_delete, args=(filepath,))
		thread.start()
