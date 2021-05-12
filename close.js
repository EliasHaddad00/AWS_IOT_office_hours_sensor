var awsIot = require('aws-iot-device-sdk');// Config
var device = awsIot.device({
   keyPath: "adec33166c-private.pem.key",
  certPath: "adec33166c-certificate.pem.crt",
    caPath: "root_ca_door.crt",
      host: "axc288okwg3o6-ats.iot.us-east-1.amazonaws.com"
});
// Connect
device
  .on('connect', function() {
    console.log('Connected');
  // Subscribe to myTopic

    device.subscribe("doorSensor");
  // Publish to myTopic
    device.publish("doorSensor", JSON.stringify({
        key1: 'Close',
    }));

  });

// Receiving a message from any topic that this device is
// subscribed to.

device
  .on('message', function(topic, payload) {
    console.log('message', topic, payload.toString());
  });

device
  .on('error', function(error) {
    console.log('Error: ', error);
  });
