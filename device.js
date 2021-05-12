var awsIot = require('aws-iot-device-sdk');// Config
var device = awsIot.device({
   keyPath: "90673f2cf3-private.pem.key",
  certPath: "90673f2cf3-certificate.pem.crt",
    caPath: "root_ca.crt",
      host: "axc288okwg3o6-ats.iot.us-east-1.amazonaws.com"
});
// Connect
device
  .on('connect', function() {
    console.log('Connected');
  // Subscribe to myTopic
    device.subscribe("myTopic");
  // Publish to myTopic
    device.publish("myTopic", JSON.stringify({
        key1: 'hello1',
        key2: 'hello2',
        key3: 'hello3'
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
