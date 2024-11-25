#!/usr/bin/env python3
from typing import Optional
from winreg import HKEY_CLASSES_ROOT

import commands.horizontal.switchmotorcalibration
import commands2.button
import wpilib
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Timer, RobotBase

from commands.ballpusher.ballpusherload import BallPusherLoad
from commands.horizontal.horizontalcalibration import HorizontalCalibration
from subsystems.ballpusher import BallPusher
from subsystems.horizontal import Horizontal
from commands.horizontal.switchmotorcalibration import SwitchMotorCalibration

loop_delay = 30.0
entry_name_check_time = "/CheckSaveLoop/time"
entry_name_check_mirror = "/CheckSaveLoop/mirror"


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # robotInit fonctionne mieux avec les tests que __init__.
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

        """
        Autonomous
        """

        self.auto_command: Optional[commands2.Command] = None
        self.auto_chooser = wpilib.SendableChooser()

        """
        Joysticks
        """

        """
        Subsystems
        """
        self.horizontal = Horizontal()
        self.ballPusher = BallPusher()

        """
        Default subsystem commands
        """

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
        pass

    def setupSubsystemOnDashboard(self):
        wpilib.SmartDashboard.putData("Shooter", self.shooter)

    def setupCommandsOnDashboard(self):
        """
        Send commands to dashboard to
        """
        putCommandOnDashboard(
            "Left Switch Calibration",
            SwitchMotorCalibration(
                self.horizontal.isAtLeftSwitch,
                self.horizontal.moveLeft,
                self.horizontal.moveRight,
                self.horizontal.stop,
            ),
        )
        putCommandOnDashboard(
            "Right Switch Calibration",
            SwitchMotorCalibration(
                self.horizontal.isAtRightSwitch,
                self.horizontal.moveRight,
                self.horizontal.moveLeft,
                self.horizontal.stop,
            ),
        )
        putCommandOnDashboard(
            "Horizontal Calibration", HorizontalCalibration(self.horizontal)
        )
        putCommandOnDashboard(
            "Ball Pusher Load", BallPusherLoad(self.ballPusher)
        )

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
