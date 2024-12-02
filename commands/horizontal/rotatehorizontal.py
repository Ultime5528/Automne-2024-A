import commands2

from subsystems.horizontal import Horizontal
from utils.safecommand import SafeCommand


class RotateHorizontal(SafeCommand):
    def __init__(
        self,
        horizontal: Horizontal,
        xbox_remote: commands2.button.CommandXboxController,
    ):
        super().__init__()
        self.horizontal = horizontal
        self.addRequirements(horizontal)
        self.xbox_remote = xbox_remote

    def execute(self) -> None:
        speed = self.xbox_remote.getLeftX()
        self.horizontal.move(speed)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.horizontal.stop()
