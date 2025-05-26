# BEE HIVE MONITOR

## Project Description
This project consists of two parts:

1. ESP32 — a device connected to WyiFi that sends sample JSON data to the MQTT broker.

2. Python MQTT Client — a Python script that subscribes to the MQTT topic, receives messages (in the future: saves the data to CSV or JSON files along with the timestamp of reception).

----------------------------------------------------

## Technical Details
1. ESP32 - Sending MQTT Data
- Connects to a WiFi network.

- Uses WiFiClientSecure for secure connection to the MQTT broker (HiveMQ Cloud).

- Publishes JSON messages every second to the topic test/esp32/random.

- Uses the root CA certificate to verify the TLS connection.

2. Python - Receiving and Saving Data
- Subscribes to the MQTT topic test/esp32/random.

- Parses incoming JSON payloads.
 
- Appends the data to a file:

   - mqtt_data.csv with columns and timestamps, or

   - mqtt_data.json as a list of JSON objects.

- Automatically adds the timestamp of message reception.
  
----------------------------------------------------

## Requirements
- ESP32 with Arduino IDE (libraries: WiFi, WiFiClientSecure, PubSubClient)

- Python 3.x

- Paho MQTT library:
  
pip install paho-mqtt

----------------------------------------------------

## Configuration
ESP32
- Set WiFi credentials.

- Enter MQTT broker details.

- Place the root CA certificate to match your broker.

Python
- Connects to the same MQTT broker.

- Subscribes to the topic.

- Saves received data into .csv or .json.

----------------------------------------------------

## Architecture
[Architecture](bee_hive_monitor_architecture.jpg)

Only one path will be chosen if a connection with the ESP32 is available
