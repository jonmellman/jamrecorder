import os

RECORDING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '../audio'))
SERVER_START_TIME = None # This gets set in the server setup... TODO how to make this better

class ValidationError(Exception):
	pass
