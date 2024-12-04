from subsystems.shooter import Shooter
from utils.safecommand import SafeCommand


class ShooterStopMotors(SafeCommand):

    def __init__(self, shooter: Shooter):
        super().__init__()

        self.shooter = shooter
        self.addRequirements(shooter)

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool):
        self.shooter.stopMotors()