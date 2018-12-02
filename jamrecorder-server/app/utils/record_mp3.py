import subprocess
import concurrent.futures
import time
import sys

# TODO: Is this the best way to have file-level variables?
this = sys.modules[__name__]
this.child_processes = {}

def start(dest_path):
	_verify_microphone()
	executor = concurrent.futures.ThreadPoolExecutor(max_workers = 1)
	future = executor.submit(_block_until_done_recording, dest_path)
	executor.shutdown(wait = False)

def _verify_microphone():
	devices_output = str(subprocess.check_output(["arecord", "--list-devices"]), "utf-8")

	# TODO: More sophisticated check
	if devices_output.count("\n") <= 1:
		raise Exception("Microphone not found") # TODO: Custom error class

def _block_until_done_recording(dest_path):
	this.child_processes["record_raw"] = subprocess.Popen([
		"arecord",
		"-f",
		"cd",
		"-t",
		"raw",
		"-D",
		"hw:1,0",
		"-d",
		"7200" # 2h timeout for safety
	], stdout = subprocess.PIPE);

	this.child_processes["mp3_convert"] = subprocess.Popen([
		"lame",
		"-r",
		"-h",
		"-m",
		"s",
		"-s",
		"44.1",
		"--signed",
		"--little-endian",
		"--bitwidth",
		"16",
		"--verbose",
		"-",
		dest_path
	], stdin=this.child_processes["record_raw"].stdout);

	this.child_processes["mp3_convert"].wait()
	# TODO: Should we check mp3_convert's exit code to see if we know whether it was terminated?
	# If it was terminated, we don't want to invoke the done callback

def interrupt():
	for _, process in this.child_processes.items():
		process.terminate()
	this.child_processes = {}
