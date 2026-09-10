"""
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python development tools and MariaDB/MySQL packages
sudo apt install python3-pip libgpiod2 mariadb-server mariadb-client python3-dev -y

# Install the Adafruit DHT library and MySQL connector via pip
pip3 install adafruit-circuitpython-dht mysql-connector-python
"""
import time
import board
import adafruit_dht

# DHT11 connected to GPIO 4 (Pin 7)
dht_device = adafruit_dht.DHT11(board.D4)

def read_sensor():
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        
        if temperature_c is not None and humidity is not None:
            temperature_f = temperature_c * (9 / 5) + 32
            print(f"Temp: {temperature_c:.1f}°C ({temperature_f:.1f}°F) | Humidity: {humidity}%")
            return temperature_c, humidity
        else:
            print("Failed to retrieve data from sensor.")
            return None, None

    except RuntimeError as error:
        # DHT sensors occasionally fail to read; this handles transient timing errors
        print(f"Sensor read error: {error.args[0]}")
        return None, None
    except Exception as error:
        dht_device.exit()
        raise error

if __name__ == "__main__":
    print("Reading DHT11 sensor data (Press Ctrl+C to exit)...")
    try:
        while True:
            read_sensor()
            time.sleep(2)  # DHT11 requires at least 2 seconds between reads
    except KeyboardInterrupt:
        print("\nProgram stopped.")
    finally:
        dht_device.exit()