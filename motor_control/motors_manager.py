import board
import busio
from adafruit_pca9685 import PCA9685
import time
from mqtt import subscriber


class MotorsManager:
    def __init__(self):
        # Initiate i2c
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c, address=0x40)
        self.pca.frequency = 1000  # 1 kHz

    def _map_duty_cycle(self, percentage):
        """Map 1-100% to 0-65535 for PCA9685"""
        if not 0 <= percentage <= 100:
            raise ValueError("Duty cycle must be between 0-100")
        return int((percentage / 100) * 65535)  # 65535

    def motorL_forward(self, duty_cycle):
        self.pca.channels[0].duty_cycle = self._map_duty_cycle(duty_cycle)
        self.pca.channels[1].duty_cycle = self._map_duty_cycle(100)
        self.pca.channels[2].duty_cycle = self._map_duty_cycle(0)

    def motorL_reverse(self, duty_cycle):
        self.pca.channels[0].duty_cycle = self._map_duty_cycle(duty_cycle)
        self.pca.channels[1].duty_cycle = self._map_duty_cycle(0)
        self.pca.channels[2].duty_cycle = self._map_duty_cycle(100)

    def motorR_forward(self, duty_cycle):
        self.pca.channels[8].duty_cycle = self._map_duty_cycle(duty_cycle)
        self.pca.channels[9].duty_cycle = self._map_duty_cycle(100)
        self.pca.channels[10].duty_cycle = self._map_duty_cycle(0)

    def motorR_reverse(self, duty_cycle):
        self.pca.channels[8].duty_cycle = self._map_duty_cycle(duty_cycle)
        self.pca.channels[9].duty_cycle = self._map_duty_cycle(0)
        self.pca.channels[10].duty_cycle = self._map_duty_cycle(100)

    def stop_all_motors(self):
        self.pca.channels[0].duty_cycle = self._map_duty_cycle(0)
        self.pca.channels[8].duty_cycle = self._map_duty_cycle(0)

    def run(self):
        try:
            while True:
                print("Kör")
                self.motorL_forward(50)
                self.motorR_forward(50)

                time.sleep(10)

        except KeyboardInterrupt:
            # Shuts downs
            self.stop_all_motors()
            print("\n\nShuts down motors")


if __name__ == "__main__":
    manager = MotorsManager()
    manager.run()
