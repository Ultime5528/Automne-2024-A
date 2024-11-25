import wpilib

from subsystems.ballpusher import BallPusher
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class BallPusherLoad(SafeCommand):

    open_time = autoproperty(0.75)

    def __init__(self, ballPusher : BallPusher) -> None:
        super().__init__()
        self.ballPusher = ballPusher
        self.addRequirements(ballPusher)
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.ballPusher.open()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.open_time

    def end(self, interrupted: bool) -> None:
        self.timer.stop()
        self.ballPusher.close()