from typing import Callable

import commands2

from utils.safecommand import SafeCommand


class Rotate(SafeCommand):

    def __init__(
        self,
        safeSubsystem,
        xbox_remote: commands2.button.CommandXboxController,
        moveDirection1: Callable[[float], None],
        moveDirection2: Callable[[float], None],
    ):
        super().__init__()
        self.addRequirements(safeSubsystem)
        self.xbox_remote = xbox_remote

    def execute(self) -> None:
        self.xbox_remote.getLeftX()


