import seaborn as sns
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from collections import deque

# --- Ustawienia MQTT ---
BROKER_IP = "localhost"  # Jeśli masz Mosquitto uruchomione lokalnie, użyj "localhost"
TOPIC = "pszczoly/dane"  # Temat MQTT


# --- Klasa MQTTClient ---
class MQTTClient:
    def __init__(self, app):
        self.app = app
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(BROKER_IP, 1883, 60)
        self.client.subscribe(TOPIC)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode("utf-8")
        Clock.schedule_once(lambda dt: self.app.update_data(data), 0)


# --- Definicja ekranów ---
class MainScreen(Screen):
    pass


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = Image(size_hint=(1, 1))
        self.add_widget(self.image)


# --- Plik KV --- (Kivy)
KV = '''
ScreenManager:
    MainScreen:
    SecondScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: 'vertical'

        # Pasek nawigacyjny
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            Button:
                text: "➡️"
                size_hint_x: None
                width: '50dp'
                on_release: app.root.current = "second"

        # Nagłówek
        Label:
            id: header
            text: "[color=00cc00][b]monitor ula[/b][/color]"
            markup: True
            font_size: "40sp"
            size_hint_y: None
            height: "60dp"
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 1
                Line:
                    rectangle: (self.x, self.y, self.width, self.height)
                    width: 2

        # Wyświetlanie danych
        BoxLayout:
            orientation: 'vertical'
            spacing: "15dp"

            Label:
                id: humidity
                text: "[color=00cc00]wilgotnosc: --%[/color]"
                markup: True
                font_size: "35sp"

            Label:
                id: temperature
                text: "[color=00cc00]temperatura: --°C[/color]"
                markup: True
                font_size: "35sp"

            Label:
                id: pressure
                text: "[color=00cc00]cisnienie: --hPa[/color]"
                markup: True
                font_size: "35sp"

            Label:
                id: vibration
                text: "[color=00cc00]czestotliwosc: --Hz[/color]"
                markup: True
                font_size: "35sp"

<SecondScreen>:
    name: "second"
    BoxLayout:
        orientation: 'vertical'

        # Pasek nawigacyjny
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            Button:
                text: "⬅️"
                size_hint_x: None
                width: '50dp'
                on_release: app.root.current = "main"
'''


# --- Aplikacja Kivy ---
class HiveMonitorApp(App):
    def build(self):
        Builder.load_string(KV)
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(SecondScreen(name="second"))

        # Inicjalizacja klienta MQTT
        self.mqtt_client = MQTTClient(self)

        # Przechowywanie ostatnich 7 pomiarów
        self.temperature_data = deque(maxlen=7)
        self.humidity_data = deque(maxlen=7)
        self.pressure_data = deque(maxlen=7)
        self.vibration_data = deque(maxlen=7)

        return self.sm

    def update_data(self, data):
        try:
            # Parsowanie danych
            data = data.strip("()")
            values = data.split(", ")
            if len(values) == 4:
                temperature = float(values[0])
                humidity = float(values[1])
                pressure = float(values[2])
                vibration = float(values[3])

                # Dodaj dane do deque
                self.temperature_data.append(temperature)
                self.humidity_data.append(humidity)
                self.pressure_data.append(pressure)
                self.vibration_data.append(vibration)

                # Aktualizacja etykiet na pierwszym ekranie
                self.sm.get_screen("main").ids.temperature.text = f"[color=00cc00]temperatura: {temperature}°C[/color]"
                self.sm.get_screen("main").ids.humidity.text = f"[color=00cc00]wilgotnosc: {humidity}%[/color]"
                self.sm.get_screen("main").ids.pressure.text = f"[color=00cc00]cisnienie: {pressure}hPa[/color]"
                self.sm.get_screen("main").ids.vibration.text = f"[color=00cc00]czestotliwosc: {vibration}Hz[/color]"

                # Generowanie wykresu
                self.create_and_update_plot()

        except Exception as e:
            print(f"Błąd przetwarzania danych: {e}")

    def create_and_update_plot(self):
        # Tworzenie wykresu za pomocą seaborn
        data = {
            'Temperatura': list(self.temperature_data),
            'Wilgotność': list(self.humidity_data),
            'Ciśnienie': list(self.pressure_data),
            'Wibracje': list(self.vibration_data)
        }

        # Użycie seaborn do stworzenia wykresu
        sns.set(style="whitegrid")

        # Zwiększono wielkość wykresu
        fig, ax = plt.subplots(figsize=(16, 20))

        # Tworzenie wykresu liniowego
        for label, values in data.items():
            ax.plot(values, label=label)

        ax.set_title("Ostatnie 7 pomiarów")
        ax.legend()

        # Zapisz wykres jako plik .png
        plot_file = "sensor_data_plot.png"
        plt.savefig(plot_file, bbox_inches='tight')

        # Zaktualizuj obraz na drugim ekranie
        second_screen = self.sm.get_screen("second")
        second_screen.image.source = plot_file
        second_screen.image.reload()


if __name__ == "__main__":
    HiveMonitorApp().run()
