from mcu_handler.communication.protocol import parse_status

class Arduino:
    def __init__(self, link):
        self.link = link

    def set_motors(self, left: int, right: int):
        """Skicka PWM till Arduino"""
        self.link.send(f"SET {left} {right}")

    def stop(self):
        """Stoppa motorerna omedelbart"""
        self.link.send("STOP")

    def read_status(self):
        """Läs senaste status från Arduino"""
        line = self.link.read()
        return parse_status(line)
