# Setup

1. `npm install`
1. `nvm use`

# Usage

1. Set environment variables `AWS_REGION` and `AWS_THING_ENDPOINT`
1. Run the server on your IoT device with `node server.js`. This listens to an mqtt message broker for requests.
1. Create a lambda to run the `client.js`. The lambda will communicate with IoT device.
