from typing import Callable

from subsystems.horizontal import Horizontal
from utils.safecommand import SafeCommand


class HorizontalCalibration(SafeCommand):

    def __init__(self, horizontal: Horizontal, isAtSwitch: Callable[[], bool], moveToSwitch: Callable[[], None], moveAwayFromSwitch: Callable[[], None]):
        super().__init__()
        self.horizontal = horizontal
        self.isAtSwitch = isAtSwitch
        self.moveToSwitch = moveToSwitch
        self.moveAwayFromSwitch = moveAwayFromSwitch
        self.addRequirements(horizontal)
        self.switch_was_pressed = False

    def initialize(self):
        self.switch_was_pressed = False

    def execute(self):
        if self.isAtSwitch():
            self.moveAwayFromSwitch()
            self.switch_was_pressed = True
        else:
            self.moveToSwitch()

    def isFinished(self) -> bool:
        return not self.isAtSwitch() and self.switch_was_pressed

    def end(self, interrupted: bool):
        self.horizontal.stop()
