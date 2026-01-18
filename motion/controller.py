"""
Controller for the motors
"""


class MotionController:
    def __init__(self, arduino):
        self.arduino = arduino

    def update(self, cmd):
        left, right = self.diff_drive(cmd.linear, cmd.angular)
        self.arduino.set_motors(left, right)

    def diff_drive(self, v, w):
        left = v - w
        right = v + w
        return self._clamp(left), self._clamp(right)

    def _clamp(self, v):
        return max(-1.0, min(1.0, v))
