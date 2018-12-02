import os
import json
from datetime import datetime
import flask
from app.recorder import Recorder
from app import constants
from app.flusher import Flusher
from app.utils import dropbox

if "MOCKS" in os.environ:
	os.environ["PATH"] = os.getcwd() + "/mocks:" + os.environ["PATH"]

constants.SERVER_START_TIME = datetime.now()
app = flask.Flask(__name__)

flusher = Flusher(dropbox.Uploader())
recorder = Recorder(flusher)

@app.route("/toggle")
def toggle():
	recorder.toggle()
	return flask.jsonify(get_status())

@app.route("/start")
def start_recording():
	try:
		recorder.start_recording()
	except constants.ValidationError:
		return flask.jsonify(get_status()), 400

	return flask.jsonify(get_status())

@app.route("/stop")
def stop_recording():
	try:
		recorder.stop_recording()
	except constants.ValidationError:
		return flask.jsonify(get_status()), 400

	return flask.jsonify(get_status())

@app.route("/status")
def status():
    return flask.jsonify(get_status())

@app.route("/flush")
def flush():
    flush_old_mp3s()
    return flask.jsonify({
		"ok": True
	})

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def get_status():
	return {
    	"recording": recorder.is_recording,
    	"filename": recorder.filename,
    	"funny_name": recorder.funny_name,
    	"start_time": str(constants.SERVER_START_TIME),
    	"uptime": str(datetime.now() - constants.SERVER_START_TIME)
    }

def flush_old_mp3s():
	def _should_flush(filepath):
		return filepath.endswith('.mp3') and _is_from_before_server_start(filepath)

	def _is_from_before_server_start(filepath):
		file_modified_time = datetime.fromtimestamp((os.path.getmtime(filepath)))
		return file_modified_time < constants.SERVER_START_TIME

	recording_directory_filepaths = [os.path.abspath(os.path.join(constants.RECORDING_DIRECTORY, filename)) for filename in os.listdir(constants.RECORDING_DIRECTORY)]
	for filepath in recording_directory_filepaths:
		if (_should_flush(filepath)):
			flusher.upload_and_delete_nonblocking(filepath)


# Upload and delete old mp3s on startup
# flush_old_mp3s()
