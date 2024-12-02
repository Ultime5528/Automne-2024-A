import commands2

from subsystems.vertical import Vertical
from utils.safecommand import SafeCommand


class RotateVertical(SafeCommand):
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
        speed = self.xbox_remote.getLeftY()
        self.vertical.move(speed)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.vertical.stop()
