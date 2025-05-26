# BEE HIVE MONITOR

## Project Description
This project consists of two parts:

1. ESP32 — a device connected to WyiFi that sends sample JSON data to the MQTT broker.

2. Python MQTT Client — a Python script that subscribes to the MQTT topic, receives messages (in the future: saves the data to CSV or JSON files along with the timestamp of reception).

----------------------------------------------------

## Technical Details
1. ESP32 - Sending MQTT Data (first path in architecture)
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

## Architecture
[Architecture](sample_architecture.jpg)

Only one path will be chosen if a connection with the ESP32 is available
