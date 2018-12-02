'use strict';

const rp = require('request-promise');
const {
	connect
} = require('./common');

const listen = Promise.coroutine(function*() {
	const client = yield connect();
	client._mqtt.subscribe('requests/+');

	client._mqtt.on('message', Promise.coroutine(function*(topic, messageBuffer) {
		const message = JSON.parse(messageBuffer.toString());

		if (topic.startsWith('requests/')) {
			console.log('Recieved request', message);
			const result = yield dispatchHttpRequest(message);

			console.log('Publishing result', result);
			const messageId = topic.split('requests/')[1];
			client.publish(`responses/${messageId}`, result);
		}
	}));
});

const dispatchHttpRequest = Promise.coroutine(function*(request) {
	let result;
	try {
		const response = yield rp({
			method: request.method,
			uri: request.url,
			json: true,
			resolveWithFullResponse: true,
			simple: false
		});

		result = {
			statusCode: response.statusCode,
			body: response.body
		};
	} catch (e) {
		result = {
			statusCode: null,
			body: null,
			error: e.toString()
		};
	}

	return result;
});

module.exports = {
	listen: listen
};

if (!module.parent) {
	listen();
}
