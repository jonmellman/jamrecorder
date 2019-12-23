# JamRecorder

JamRecorder is an Alexa skill for hands-free audio recording and sharing. It records audio to a local Raspberry Pi device and automatically uploads the result to DropBox.

![JamRecorder image](/image.png)

I deployed it in a music rehearsal room that I share with friends, and it makes our lives easier with these features:

## Features:
* Hands-free recording ("Alexa, ask JamRecorder to start recording"). This is important since I'm often tethered to cables and my hands are occupied.
* High-quality recordings using an external USB microphone.
* Recordings are automatically uploaded to Dropbox for easy sharing. I printed out a QR code that links to the Dropbox folder and taped it to the wall of our rehearsal room, so it's easy for anyone to find their recordings.
* Fun auto-generated song names.

## Usage Example
Me: "Alexa, ask JamRecorder to start recording"

Alexa: "Okay, I'm now recording. I named your song: Fat Sneeze"

Me: 🎶🎸🥁🎷🎶🎸🥁🎷

Me: "Okay Alexa, ask JamRecorder to stop recording"

Alexa: "Okay, I stopped recording and am uploading your song to Dropbox."

Me: 🤙

## Technical Details
JamRecorder is comprised of three independent parts that each live in their own directory:
1. `alexa/` - A AWS Lambda function built with the NodeJS Alexa SDK. This script is simply the hosted front-end for communicating messages to the jamrecorder server. It contains the logic for converting speech keywords to iot-communicator calls.
1. `iot-communicator/` - A NodeJS library for relaying messages from the Alexa Lambda function to the JamRecorder Server running on the local Raspberry Pi. It facilitates RPC-like communication by wrapping AWS IoT's MQQT client.
1. `jamrecorder-server/` - A Python Flask server, running on a local Raspberry Pi connected to a USB microphone, that hosts an API responsible for interfacing with the microphone, recording to a micro SD, uploading recordings to Dropbox, and flushing the recording from disk.
