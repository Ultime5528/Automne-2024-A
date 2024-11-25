from typing import Final

"""
Respect the naming convention : "subsystem" _ "component type" _ "precision"

Put port variables into the right category: CAN - PWM - DIO

Order port numbers, ex:
    drivetrain_motor_fl: Final = 0
    drivetrain_motor_fr: Final = 1
    drivetrain_motor_rr: Final = 2
"""

# CAN

# PWM
shooter_motor_left: Final = 0
shooter_motor_right: Final = 1
horizontal_motor: Final = 2
vertical_motor: Final = 3
ball_pusher_motor: Final = 4

# DIO
horizontal_switch_left: Final = 0
horizontal_switch_right: Final = 1
horizontal_encoder_a: Final = 2
horizontal_encoder_b: Final = 3
