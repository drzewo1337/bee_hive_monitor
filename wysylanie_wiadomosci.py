import paho.mqtt.client as mqtt
import time
import random

# Ustawienia brokera
BROKER_IP = "localhost"  # Jeśli masz Mosquitto uruchomione lokalnie, użyj "localhost"
TOPIC = "pszczoly/dane"  # Temat, do którego aplikacja będzie wysyłać dane

# Funkcja callback wywoływana po połączeniu z brokerem
def on_connect(client, userdata, flags, rc):
    print(f"Połączono z brokerem, kod: {rc}")

# Funkcja callback wywoływana po wysłaniu wiadomości
def on_publish(client, userdata, mid):
    print(f"Wiadomość wysłana, id: {mid}")

# Tworzymy klienta MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Łączymy się z brokerem
client.connect(BROKER_IP, 1883, 60)

# Rozpoczynamy pętlę nasłuchującą
client.loop_start()

# Pętla wysyłająca dane co 2 sekundy
while True:
    temperature = random.randint(10, 20)
    humility = random.randint(30, 40)
    weight = random.randint(50, 60)
    vibration = random.randint(70, 80)

    payload = f"{temperature, humility, weight, vibration}"  # Prosty payload z timestampem
    client.publish(TOPIC, payload)  # Wysyłamy wiadomość na temat
    print(f"Wysłano wiadomość: {payload}")
    time.sleep(2)  # Czekamy 2 sekundy przed wysłaniem kolejnej wiadomości
