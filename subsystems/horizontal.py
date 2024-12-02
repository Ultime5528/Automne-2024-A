import wpilib
from wpilib import VictorSP, RobotBase
from wpilib.simulation import PWMSim, EncoderSim

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.switch import Switch


class Horizontal(SafeSubsystem):
    motor_position_min = autoproperty(0.0)
    motor_position_max = autoproperty(65.0)
    speed = autoproperty(1.0)

    def __init__(self):
        super().__init__()

        self._motor = VictorSP(ports.horizontal_motor)

        self._switch_left = Switch(
            Switch.Type.NormallyClosed, ports.horizontal_switch_left
        )
        self._switch_right = Switch(
            Switch.Type.NormallyClosed, ports.horizontal_switch_right
        )
        self._encoder = wpilib.Encoder(
            ports.horizontal_encoder_a,
            ports.horizontal_encoder_b,
            reverseDirection=True,
        )

        self.isInCalibrationMode = False

        self.addChild("motor", self._motor)
        self.addChild("encoder", self._encoder)

        self._offset = 0.0
        self._has_reset = False
        self._prev_is_down = False
        self._prev_is_up = False

        if RobotBase.isSimulation():
            self._sim_motor = PWMSim(self._motor)
            self._sim_encoder = EncoderSim(self._encoder)
            self._encoder.setDistancePerPulse(0.03)

    def isAtLeftSwitch(self):
        return self._switch_left.isPressed()

    def isAtRightSwitch(self):
        return self._switch_right.isPressed()

    def stop(self):
        self._motor.stopMotor()

    def moveRight(self):
        self.move(self.speed)

    def moveLeft(self):
        self.move(-self.speed)

    def move(self, speed: float):
        if self.isAtRightSwitch() and speed > 0:
            speed = 0
        elif self.isAtLeftSwitch() and speed < 0:
            speed = 0

        self._motor.set(speed)

    def simulationPeriodic(self) -> None:

        self._sim_encoder.setDistance(
            self._sim_encoder.getDistance() + self._motor.get()
        )

        if self.getMotorPosition() < self.motor_position_min:
            self._switch_left.setSimPressed()
        else:
            self._switch_left.setSimUnpressed()

        if self.getMotorPosition() > self.motor_position_max:
            self._switch_right.setSimPressed()
        else:
            self._switch_right.setSimUnpressed()

    def getMotorPosition(self):
        return self._encoder.getDistance()

    def setCalibrationOn(self):
        self.isInCalibrationMode = True

    def setCalibrationOff(self):
        self.isInCalibrationMode = False
