from wpilib import VictorSP

import ports
from utils.safesubsystem import SafeSubsystem


class Conveyor(SafeSubsystem):
    def __init__(self):
        super().__init__()
        self.motor = VictorSP(ports.horizontal_motor)

    def push(self):
        pass
