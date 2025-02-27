import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import messagebox

BAUDRATE = 115200

def find_esp32_port():
    """Automatycznie wykrywa port ESP32."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "CP210" in port.description or "CH340" in port.description:
            print(f"Znaleziono ESP32 na porcie {port.device}")
            return port.device
    return None

def send_config():
    """Wysyła konfigurację do ESP32 przez USB."""
    esp32_port = find_esp32_port()
    if not esp32_port:
        messagebox.showerror("Błąd", "ESP32 nie znaleziono! Sprawdź połączenie USB.")
        return

    host = host_entry.get().strip()
    port = port_entry.get().strip()

    if not (host and port):
        messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    config_data = f"HOST={host};PORT={port}\n"

    try:
        ser = serial.Serial(esp32_port, BAUDRATE, timeout=1)
        time.sleep(2)
        ser.write(config_data.encode())
        response = ser.readline().decode().strip()
        ser.close()

        messagebox.showinfo("Sukces", f"Odpowiedź ESP32: {response}")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))

# Tworzenie okna GUI
root = tk.Tk()
root.title("Konfiguracja ESP32")
root.geometry("350x200")

tk.Label(root, text="Host:").pack()
host_entry = tk.Entry(root)
host_entry.pack()

tk.Label(root, text="Port:").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Button(root, text="Wyślij konfigurację", command=send_config).pack(pady=10)

root.mainloop()
