from wpilib import VictorSP

import ports
from utils.safesubsystem import SafeSubsystem


class Horizontal(SafeSubsystem):
    def __init__(self):
        super().__init__()

        self.motor = VictorSP(ports.horizontal_motor)

    def moveRight(self):
        pass

    def moveLeft(self):
        pass
