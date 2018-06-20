#Raspberry Pi Code
#GCP Code included

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.cloud import pubsub_v1
from google.cloud import storage
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
from Adafruit_BME280 import *

import datetime
import os
import random
import ssl
import time
import calendar

#set up the sensor for reading temp/pressure/humidity
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8,
h_mode=BME280_OSAMPLE_8)

gcpBucket = "arch_term_proj_bucket"

def gpioSetup():
#setup number to broadcom scheme
gpio.setmode(gpio.BCM)

#for when a connection is established to mqtt server
def connectionStatus(client, userdata, flags, rc):

#subscribe to topic
mqttClient.subscribe("rpi/gpio")
mqttClient.subscribe("sensory")

#Uploads a file to the GCP via bucket storage ****** GCP CODE ******
def upload_blob(bucketName, sourceFileName, destinationBlobName):

storageClient = storage.Client()
bucket = storageClient.get_bucket(bucketName)
blob = bucket.blob(destinationBlobName)
blob.upload_from_filename(sourceFileName)
print('File {} uploaded to {}.'.format(sourceFileName, destinationBlobName))

#for when a message is recieved by the mqtt server
def messageDecoder(client, userdata, msg):

gpioSetup()

#Decode message recieved
message = msg.payload.decode(encoding='UTF-8')

#set GPIO pin to HIGH or LOW to turn on or off appliances/relay/LED
if message == "LIGHTSON":
gpio.setwarnings(False)
gpio.setup(21, gpio.OUT)
gpio.output(21, gpio.HIGH)
print("Lamp is ON!")


#since 5V pin is always high or always low the standard method of sending a high or low signal doesn't work.
#Thus the only way to shut off the relay without wiping the whole board and everything else that is on is
#to change the pin to an input rather than an output.

elif message == "LIGHTSOFF":
gpio.setup(21,gpio.IN)
print("Lamp is OFF!")

elif message == "HEATLEDON":
gpio.setwarnings(False)
gpio.setup(26, gpio.OUT)
gpio.output(26, gpio.HIGH)
print("Heat LED is ON!")

elif message == "HEATLEDOFF":
gpio.setup(26,gpio.OUT)
gpio.output(26, gpio.LOW)
print("Heat LED is OFF!")

elif message == "HUMIDLEDON":
gpio.setwarnings(False)
gpio.setup(19, gpio.OUT)
gpio.output(19, gpio.HIGH)
print("Humidifier LED is ON!")

elif message == "HUMIDLEDOFF":
gpio.setup(19, gpio.OUT)
gpio.output(19, gpio.LOW)
print("Humidifier LED is OFF!")

#prompts the BME280 chip for sensory data and prints/publishes the data to the iOS device
elif message == "TEMP":
degrees = sensor.read_temperature()
print 'Temp = {0:0.3f} deg C'.format(degrees)
mqttClient.publish("rpi-temp", "{0:0.2f} °C".format(degrees), qos=1)

elif message == "HUMID":
degrees = sensor.read_temperature()
humidity = sensor.read_humidity()
print 'Humidity = {0:0.2f} %'.format(humidity)
mqttClient.publish("rpi-humid", "{0:0.2f} %".format(humidity), qos=1)

elif message == "PRESS":
degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
print 'Pressure = {0:0.2f} hPa'.format(hectopascals)
mqttClient.publish("rpi-press", "{0:0.2f} hPa".format(hectopascals), qos=1)

#prompts the RaspberryPi to send sensory data from all three categories to a log file long with a date and time of prompt
elif message == "UPDATELOG":
degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()
print 'Temp = {0:0.3f} deg C'.format(degrees)
print 'Pressure = {0:0.2f} hPa'.format(hectopascals)
print 'Humidity = {0:0.2f} %'.format(humidity)
f = open('Templog.txt','a')

f.write(time.strftime("%A, %B %d %Y %H:%M:%S",time.localtime(None)) + '\nTemperature = ' + str('{0:0.2f}'.format(degrees)) + ' °C \nAir Pressure = ' + str('{0:0.2f}'.format(hectopascals) +' hPa \nHumidity = '+ str('{0:0.2f}'.format(humidity) + '%\n\n')))

f.close()

#Use of the GCP code
upload_blob(gcpBucket, 'Templog.txt', 'Sensor_Log.txt')

#fun default message incase the user somehow finds a way to publish/subscribe to an unsanctioned message
else:
print("I honestly have no idea how you came to this message. Thank you forplaying my game.")

#setup GPIO pins
gpioSetup()

#set client name
clientName = "RasPiNursery"

#Set MQTT server address
serverAddress = "XXX.XXX.X.XXX" #home IPv6

#instantiate paho as mqtt client
mqttClient = mqtt.Client(clientName)

#set the calling functions
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

#Connect and stay active functions
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
