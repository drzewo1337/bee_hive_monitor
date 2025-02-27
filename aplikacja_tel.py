from kivy.lang import Builder
from kivymd.app import MDApp  # Użyj MDApp z KivyMD
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

# Twoja aplikacja
class MyApp(MDApp):  # Dziedziczenie po MDApp z KivyMD
    def build(self):
        # Layout aplikacji
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Pole tekstowe na adres brokera
        self.broker_host_input = MDTextField(hint_text="Broker Host", size_hint=(1, 0.1))
        layout.add_widget(self.broker_host_input)

        # Pole tekstowe na port
        self.broker_port_input = MDTextField(hint_text="Broker Port", size_hint=(1, 0.1))
        layout.add_widget(self.broker_port_input)

        # Przycisk do połączenia z brokerem
        connect_button = MDRaisedButton(text="Connect", size_hint=(1, 0.1), on_press=self.connect_to_broker)
        layout.add_widget(connect_button)

        return layout

    def connect_to_broker(self, instance):
        # Funkcja łącząca z brokerem, która po naciśnięciu przycisku wyświetli dane w konsoli
        broker_host = self.broker_host_input.text
        broker_port = self.broker_port_input.text
        print(f"Connecting to broker at {broker_host}:{broker_port}")

# Uruchomienie aplikacji
if __name__ == "__main__":
    MyApp().run()
