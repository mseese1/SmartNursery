# SmartNursery

Smart Nursery is a simple application which runs on multiple platforms to monitor sensory data in a given location using a Raspberry Pi, and switch on and off appliances.  The application does require some hardware set up that will take a small amount of electrical knowledge unless by some miraculous event you happen to have a few 5v relay switches wired to 125v receptacles with outputs for GPIO at the given location.

**main.py**
This is the python code meant to run on the Raspberry Pi module.

**#Input Variables**
- degrees → data received from BME280 on temperature
- humidity → data revieved from BME280 on humidity
- pascals →data received from BME280 on pressure
- hectopascals → converted from pascals; used to display pressure data
- f → a variable used to open/append/close the log file
- mqttClient → instantiates a transaction client for publishing/subscribing to messages
- message → used to store the MQTT payload of a received message

**#Output Variables**
- gcpBucket → a global value used to identify the storage bucket to upload log files to
- f → a variable used to open/append/close the log file
- clientName → Identifies the device with the MQTT broker
- serverAddress → IPv6 address of the client connecting to the broker
- mqttClient → instantiates a transaction client for publishing/subscribing to messages

