import threading
import subprocess
import sys

# Funkcja do uruchomienia hive_monitor_app.py
def run_kivy_app():
    subprocess.run([sys.executable, "glowna_aplikacja.py"])


# Funkcja do uruchomienia test_publisher.py
def run_publisher():
    subprocess.run([sys.executable, "wysylanie_wiadomosci.py"])

# Główny blok kodu
if __name__ == "__main__":
    # Tworzymy dwa wątki: jeden do publikowania, drugi do aplikacji Kivy
    thread_publisher = threading.Thread(target=run_publisher)
    thread_kivy = threading.Thread(target=run_kivy_app)

    # Uruchamiamy oba wątki
    thread_publisher.start()
    thread_kivy.start()

    # Czekamy na zakończenie obu wątków (jeśli chcemy poczekać na ich zakończenie)
    thread_publisher.join()
    thread_kivy.join()
