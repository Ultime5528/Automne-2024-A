from typing import Callable

from utils.safecommand import SafeCommand


class SwitchMotorCalibration(SafeCommand):

    def __init__(
        self,
        isAtSwitch: Callable[[], bool],
        moveToSwitch: Callable[[], None],
        moveAwayFromSwitch: Callable[[], None],
        stop: Callable[[], None],
    ):
        super().__init__()
        self.isAtSwitch = isAtSwitch
        self.moveToSwitch = moveToSwitch
        self.moveAwayFromSwitch = moveAwayFromSwitch
        self.stop = stop
        self.switch_was_pressed = False

    def initialize(self) -> None:
        self.switch_was_pressed = False

    def execute(self) -> None:
        if self.isAtSwitch():
            self.moveAwayFromSwitch()
            self.switch_was_pressed = True
        else:
            self.moveToSwitch()

    def isFinished(self) -> bool:
        return not self.isAtSwitch() and self.switch_was_pressed

    def end(self, interrupted: bool) -> None:
        self.stop()
