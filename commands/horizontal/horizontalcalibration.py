from typing import Callable

import commands2

from commands.horizontal.switchmotorcalibration import SwitchMotorCalibration
from subsystems.horizontal import Horizontal
from utils.safecommand import SafeCommand, SafeMixin


class HorizontalCalibration(SafeMixin, commands2.SequentialCommandGroup):

    def __init__(self, horizontal: Horizontal) -> None:
        super().__init__(
            SwitchMotorCalibration(
                horizontal.isAtRightSwitch,
                horizontal.moveRight,
                horizontal.moveLeft,
                horizontal.stop,
            ),

            SwitchMotorCalibration(
                horizontal.isAtLeftSwitch,
                horizontal.moveLeft,
                horizontal.moveRight,
                horizontal.stop,
            ),
        )
        self.horizontal = horizontal
