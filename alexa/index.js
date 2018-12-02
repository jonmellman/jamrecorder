'use strict';

const Alexa = require('alexa-sdk');
const Promise = require('bluebird');
const client = require('iot-communicator/client');
const APP_ID = 'amzn1.ask.skill.a750c280-d256-41b2-8b66-c53ca69e7d4d';

const handlers = {
	LaunchRequest: function() {
		this.emit('StatusIntent');
	},
	StatusIntent: Promise.coroutine(function*() {
		const { body, error } = yield client.request('GET', 'http://localhost:5000/status');

		if (error) {
			handleRaspberryPiServerError(this, error);
			return;
		}

		if (body.recording) {
			const name = body.funny_name;
			this.emit(':tell', `Currently recording ${name}`);
		} else {
			this.emit(':tell', 'I am not recording.');
		}
	}),
	StartRecordingIntent: Promise.coroutine(function*() {
		const { body, error, statusCode } = yield client.request('GET', 'http://localhost:5000/start');

		if (error) {
			handleRaspberryPiServerError(this, error);
			return;
		}

		if (statusCode === 400) {
			const name = body.funny_name;
			this.emit(':tell', `I'm already recording ${name}`);
			return;
		}

		if (statusCode === 200 && body.recording) {
			const name = body.funny_name;
			this.emit(':tell', `I am now recording. I named your song ${name}`);
			return;
		}

		this.emit(':tell', 'Something went wrong.');
	}),
	StopRecordingIntent: Promise.coroutine(function*() {
		const { body, error, statusCode } = yield client.request('GET', 'http://localhost:5000/stop');

		if (error) {
			handleRaspberryPiServerError(this, error);
			return;
		}

		if (statusCode === 400) {
			this.emit(':tell', `I wasn't recording.`);
			return;
		}

		if (statusCode === 200 && !body.recording) {
			this.emit(':tell', 'Okay, I stopped recording.');
			return;
		}

		this.emit(':tell', 'Something went wrong.');
	})
};

function handleRaspberryPiServerError(alexa, error) {
	console.error(error);
	alexa.emit(':tell', 'I couldn\'t talk to recording server on the raspberry pi.');
}

exports.handler = function(event, context, callback) {
	const alexa = Alexa.handler(event, context, callback);
	alexa.appId = APP_ID;
	alexa.registerHandlers(handlers);

	// We need to force aws-signature-v4 to not try to add a security token header,
	// because aws-mqtt actually does it correctly.
	delete process.env.AWS_SESSION_TOKEN;

	alexa.execute();
};

if (!module.parent) {
	client.request('GET', 'http://localhost:5000/status')
		.then(function(result) {
			console.log('got result!');
			console.log(JSON.stringify(result, null, 4));
		});
}
