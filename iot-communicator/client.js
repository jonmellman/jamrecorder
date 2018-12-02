'use strict';

const {
	connect
} = require('./common');

const request = Promise.coroutine(function*(method, url, body = null) {
	const client = yield connect();

	const requestId = Date.now();
	const payload = {
		method,
		url,
		body
	};

	client.publish(`requests/${requestId}`, payload);
	const response = yield client.awaitMessage(`responses/${requestId}`);
	client.end();
	return response;
});

module.exports = {
	request: request
};

if (!module.parent) {
	request('GET', 'http://localhost:5000/status')
		.then(function(data) {
			console.log(data);
			let { error } = data;
			console.log(error);
			console.log(data);
		});
}
