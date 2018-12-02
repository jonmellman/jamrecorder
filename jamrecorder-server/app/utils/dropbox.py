import subprocess
import os

class Uploader:
	def __init__(self):
		self.remote_dir = ""

		if "MOCKS" in os.environ:
			self.remote_dir = "/test"

	def upload(self, src_path):
		filename = os.path.basename(src_path)
		dest_path = os.path.join(self.remote_dir, filename)
		return upload(
			src_path,
			dest_path
		)

def upload(src_path, dest_path):
	exit_code = subprocess.call([
		"./dropbox_uploader.sh",
		"-p",
		"upload",
		src_path,
		dest_path
	]);

	if exit_code != 0:
		raise Exception("Unexpected error during upload")
