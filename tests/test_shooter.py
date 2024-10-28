import rev
from pytest import approx
from wpilib.simulation import stepTiming

from commands.shooter.manualshoot import ManualShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from robot import Robot


def test_WaitForSpeed(control, robot):
    # For the moment, we only test that the command does not crash.
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = WaitShootSpeed(robot.shooter)
        cmd.schedule()

        counter = 0

        while cmd.isScheduled() and counter < 200:
            robot.shooter.shoot(1500)
            stepTiming(0.05)
            counter += 1

        assert counter < 200, "Command takes too long to finish"
        assert not cmd.isScheduled()


def test_ports(control, robot):
    with control.run_robot():
        assert robot.shooter._left_motor.getDeviceId() == 1
        assert robot.shooter._right_motor.getDeviceId() == 2


def test_settings(control, robot):
    with control.run_robot():
        # left
        assert not robot.shooter._left_motor.getInverted()
        assert (
            robot.shooter._left_motor.getMotorType()
            == rev.CANSparkMax.MotorType.kBrushless
        )
        assert (
            robot.shooter._left_motor.getIdleMode() == rev.CANSparkMax.IdleMode.kCoast
        )
        # right
        assert robot.shooter._right_motor.getInverted()
        assert (
            robot.shooter._right_motor.getMotorType()
            == rev.CANSparkMax.MotorType.kBrushless
        )
        assert (
            robot.shooter._right_motor.getIdleMode() == rev.CANSparkMax.IdleMode.kCoast
        )


def test_requirements(control, robot):
    with control.run_robot():
        cmd = ManualShoot(robot.shooter)
        assert cmd.hasRequirement(robot.shooter)
        cmd = WaitShootSpeed(robot.shooter)
        assert not cmd.hasRequirement(robot.shooter)
