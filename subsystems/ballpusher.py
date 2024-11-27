import wpilib

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem


class BallPusher(SafeSubsystem):
    servo_angle_open = autoproperty(90)
    servo_angle_close = autoproperty(0)

    def __init__(self):
        super().__init__()
        self.servo = wpilib.Servo(ports.ball_pusher_motor)

    def close(self):
        self.servo.setAngle(self.servo_angle_close)

    def open(self):
        self.servo.setAngle(self.servo_angle_open)
