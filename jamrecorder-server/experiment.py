from app.flusher import Flusher
from app.utils.dropbox import Uploader as DropboxUploader
from app import constants
import os

flusher = Flusher(DropboxUploader())
print("Flushing!")
flusher.flush_nonblocking(os.path.join(constants.RECORDING_DIRECTORY, "foobar.txt"))
print("Done!")
