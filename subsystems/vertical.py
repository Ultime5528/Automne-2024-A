from wpilib import VictorSP

import ports
from utils.safesubsystem import SafeSubsystem


class Vertical(SafeSubsystem):
    def __init__(self):
        super().__init__()
        self.motor = VictorSP(ports.vertical_motor)

    def moveUp(self):
        pass

    def moveDown(self):
        pass
