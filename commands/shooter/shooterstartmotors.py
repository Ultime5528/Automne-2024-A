from subsystems.shooter import Shooter
from utils.safecommand import SafeCommand


class ShooterStartMotors(SafeCommand):

    def __init__(self, shooter: Shooter):
        super().__init__()

        self.shooter = shooter
        self.addRequirements(shooter)

    def initialize(self) -> None:
        self.shooter.startMotors()

    def isFinished(self) -> bool:
        return False
