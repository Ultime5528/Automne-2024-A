import wpilib
from wpilib import VictorSP, RobotBase
from wpilib.simulation import PWMSim, EncoderSim

import ports
from utils.safesubsystem import SafeSubsystem
from utils.switch import Switch


class Horizontal(SafeSubsystem):
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
        self._motor.set(1.0)

    def moveLeft(self):
        self._motor.set(-1.0)
