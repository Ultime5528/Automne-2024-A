#!/usr/bin/env python3
from typing import Optional

import commands2.button
import wpilib
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Timer, RobotBase

from commands.ballpusher.ballpusherload import BallPusherLoad
from commands.horizontal.rotatehorizontal import RotateHorizontal
from commands.shooter.shooterstartmotors import ShooterStartMotors
from commands.shooter.shooterstopmotors import ShooterStopMotors
from commands.vertical.rotatevertical import RotateVertical
from subsystems.ballpusher import BallPusher
from subsystems.horizontal import Horizontal
from subsystems.shooter import Shooter
from subsystems.vertical import Vertical

loop_delay = 30.0
entry_name_check_time = "/CheckSaveLoop/time"
entry_name_check_mirror = "/CheckSaveLoop/mirror"


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # robotInit fonctionne mieux avec les tests que __init__.
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)

        """
        Autonomous
        """
        self.auto_command: Optional[commands2.Command] = None
        self.auto_chooser = wpilib.SendableChooser()

        """
        Joysticks
        """
        self.xbox_remote = commands2.button.CommandXboxController(0)

        """
        Subsystems
        """
        self.horizontal = Horizontal()
        self.vertical = Vertical()
        self.ballPusher = BallPusher()
        self.shooter = Shooter()

        """
        Default subsystem commands
        """
        self.horizontal.setDefaultCommand(
            RotateHorizontal(self.horizontal, self.xbox_remote)
        )
        self.vertical.setDefaultCommand(
            RotateVertical(self.vertical, self.xbox_remote)
        )
        """
        NetworkTables entries for properties save loop check
        """
        inst = NetworkTableInstance.getDefault()
        self.entry_check_time = inst.getEntry(entry_name_check_time)
        self.entry_check_mirror = inst.getEntry(entry_name_check_mirror)
        self.timer_check = Timer()
        self.timer_check.start()

        """
        Setups
        """
        self.setupButtons()
        # self.setupSubsystemOnDashboard()
        self.setupCommandsOnDashboard()

    def setupButtons(self):
        """
        Bind commands to buttons on controllers and joysticks
        """
        self.xbox_remote.a().onTrue(ShooterStartMotors(self.shooter))
        self.xbox_remote.b().onTrue(ShooterStopMotors(self.shooter))
        self.xbox_remote.rightTrigger().onTrue(BallPusherLoad(self.ballPusher))

    def setupSubsystemOnDashboard(self):
        #wpilib.SmartDashboard.putData("Shooter", self.shooter)
        pass

    def setupCommandsOnDashboard(self):
        """
        Send commands to dashboard to
        """
        putCommandOnDashboard(
            "Vertical", RotateVertical(self.vertical, self.xbox_remote)
        )
        putCommandOnDashboard(
            "Horizontal", RotateHorizontal(self.horizontal, self.xbox_remote)
        )
        putCommandOnDashboard("Ball Pusher", BallPusherLoad(self.ballPusher))

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def teleopInit(self):
        if self.auto_command:
            self.auto_command.cancel()

    def robotPeriodic(self):
        self.checkPropertiesSaveLoop()
        super().robotPeriodic()

    def checkPropertiesSaveLoop(self):
        from utils.property import mode, PropertyMode

        if not RobotBase.isSimulation() and mode != PropertyMode.Local:
            if DriverStation.isFMSAttached():
                if self.timer_check.advanceIfElapsed(10.0):
                    wpilib.reportWarning(
                        f"FMS is connected, but PropertyMode is not Local: {mode}"
                    )
            elif DriverStation.isDSAttached():
                self.timer_check.start()
                current_time = wpilib.getTime()
                self.entry_check_time.setDouble(current_time)
                if self.timer_check.advanceIfElapsed(loop_delay):
                    mirror_time = self.entry_check_mirror.getDouble(0.0)
                    if current_time - mirror_time < 5.0:
                        print("Save loop running")
                    else:
                        raise RuntimeError(
                            f"Save loop is not running ({current_time=:.2f}, {mirror_time=:.2f})"
                        )


def putCommandOnDashboard(
    sub_table: str, cmd: commands2.Command, name: str = None, suffix: str = " commands"
) -> commands2.Command:
    if not isinstance(sub_table, str):
        raise ValueError(
            f"sub_table should be a str: '{sub_table}' of type '{type(sub_table)}'"
        )

    if suffix:
        sub_table += suffix

    sub_table += "/"

    if name is None:
        name = cmd.getName()
    else:
        cmd.setName(name)

    wpilib.SmartDashboard.putData(sub_table + name, cmd)

    return cmd
