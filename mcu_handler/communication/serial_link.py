import serial
import time

class SerialLink:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=0.1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        print("Serial link initiated")

    def send(self, line: str):
        if not line.endswith("\n"):
            line += "\n"
        self.ser.write(line.encode('utf-8'))

    def read(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                return line
        except Exception as e:
            print("Serial read error:", e)
        return None

    def close(self):
        self.ser.close()
        print("Serial link closed")
