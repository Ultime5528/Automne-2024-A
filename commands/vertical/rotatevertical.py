import commands2

from subsystems.vertical import Vertical
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class RotateVertical(SafeCommand):
    vertical_speed = autoproperty(0.25)

    def __init__(
        self,
        vertical: Vertical,
        xbox_remote: commands2.button.CommandXboxController,
    ):
        super().__init__()
        self.vertical = vertical
        self.addRequirements(vertical)
        self.xbox_remote = xbox_remote

    def execute(self) -> None:
        speed = self.xbox_remote.getRightY()*self.vertical_speed
        self.vertical.move(speed)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.vertical.stop()
