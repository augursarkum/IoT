"""
SQL Query

-- Create Database
CREATE DATABASE sensor_db;

-- Create User and grant permissions (Replace 'your_password' with a secure password)
CREATE USER 'pi_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON sensor_db.* TO 'pi_user'@'localhost';
FLUSH PRIVILEGES;

-- Switch to database
USE sensor_db;

-- Create Table
CREATE TABLE dht11_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL
);

EXIT;


"""
import time
import board
import adafruit_dht
import mysql.connector

# Initialize DHT11 on GPIO 4
dht_device = adafruit_dht.DHT11(board.D4)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'pi_user',
    'password': 'your_password',  # Replace with the password set in Step 3
    'database': 'sensor_db'
}

def log_data():
    try:
        # Read values from sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            # Connect to MySQL database
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor()

            # Insert query
            query = "INSERT INTO dht11_readings (temperature, humidity) VALUES (%s, %s)"
            cursor.execute(query, (temperature, humidity))
            
            db_connection.commit()
            print(f"Logged to Database -> Temp: {temperature}°C | Humidity: {humidity}%")

            cursor.close()
            db_connection.close()
        else:
            print("Skipping database entry due to invalid sensor reading.")

    except RuntimeError as error:
        # Handle transient DHT read failures
        print(f"Sensor reading error: {error.args[0]}")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

if __name__ == "__main__":
    print("Starting sensor logger...")
    try:
        while True:
            log_data()
            time.sleep(10)  # Logs data every 10 seconds
    except KeyboardInterrupt:
        print("\nLogging stopped.")
    finally:
        dht_device.exit()


"""
Read DB values
sudo mariadb -u pi_user -p sensor_db -e "SELECT * FROM dht11_readings ORDER BY id DESC LIMIT 5;"
"""