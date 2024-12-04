import wpilib

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem


class Shooter(SafeSubsystem):

    motor_speed = autoproperty(1)

    def __init__(self):

        super().__init__()

        self._motor_left = wpilib.VictorSP(ports.shooter_motor_left)
        self._motor_right = wpilib.VictorSP(ports.shooter_motor_right)

    def startMotors(self):
        self._motor_left.set(self.motor_speed)
        self._motor_right.set(-self.motor_speed)

    def stopMotors(self):
        self._motor_left.stopMotor()
        self._motor_right.stopMotor()

