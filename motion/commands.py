"""
Commands for the motors
"""

class MotionCommand:
    def __init__(self, linear=0.0, angular=0.0):
        self.linear = linear      # m/s (eller normaliserad)
        self.angular = angular    # rad/s
