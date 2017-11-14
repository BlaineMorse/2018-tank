#!/usr/bin/env python3

import magicbot #Witchcraft to make the robot work
import wpilib #import the parts of the robot

from robotpy_ext.control.button_debouncer import ButtonDebouncer #Import the button press limiter
from networktables.util import ntproperty #Import the teleop networking stuff
from components import drive #import the drive bit of components, which is nice, if I say so myself

from robotpy_ext.common_drivers import navx #import control of navegation chip

from networktables.networktable import NetworkTable #import the Network Table

class MyRobot(magicbot.MagicRobot): #Make my robot
    mode = 'tankdrive' #set drive mode to tankdrive (the best drive)
    counter = 0 #make a counter
    #drive = drive.Drive
    """Make the basic components"""
    def createObjects(self): #creates the objects
        # NavX (purple board on top of the RoboRIO)
        # self.navX = navx.AHRS.create_spi()

        #Init the SmartDash
        self.sd = NetworkTable.getTable('SmartDashboard') #Lazy and replace getting  table with sd

        #Joysticks
        #self.left_joystick = wpilib.Joystick(0)
        #self.right_joystick = wpilib.Joystick(1)
        self.joystick = wpilib.Joystick(0)
        self.switch = ButtonDebouncer(self.joystick, 1)
        #TODO: Motors
        self.lf_motor = wpilib.Victor(0) #Set motors with repective parts
        self.lr_motor = wpilib.Victor(1)
        self.rf_motor = wpilib.Victor(2)
        self.rr_motor = wpilib.Victor(3)

        #TODO: Drivetrain object

            #self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)

    def autonomous(self):
        """PREP For autonomous mode"""
        pass #Nevermind fam

    def disabledPeriodic(self):
        """Do repeatedly while disabled"""
        pass #Nothing

    def disabledInit(self):
        """Do once immediately when robot disabled"""

    def teleopInit(self):
        "do when teleop is started"
        pass
    def teleopPeriodic(self):
        #Do like, a bajillion times a second
        """Repeat this as many times as possible while robot on teleop mode"""
            #self.drive.move(-self.left_joystick.getY(), self.right_joystick.getX())
            #leftStick, leftAxis, rightStick, rightAxis
            #self.robot_drive.tankDrive(self.joystick, 1, self.joystick, 3)

            #if self.counter%1000 == 0:
                #print(self.joystick.getRawAxis(1))
                #print(self.mode)
        if self.mode == 'tankdrive': #If the robot is set for a reasonable drive mode
            self.lf_motor.set(-1*self.joystick.getRawAxis(1)) #SET the motors
            self.lr_motor.set(-1*self.joystick.getRawAxis(1))
            self.rf_motor.set(self.joystick.getRawAxis(3))
            self.rr_motor.set(self.joystick.getRawAxis(3))
        elif self.mode == 'arcade':
            self.steering = self.joystick.getRawAxis(2) + 1 #SET the motors
            self.power = self.joystick.getRawAxis(1)
            self.lf_motor.set(-self.power* self.steering)
            self.lr_motor.set(-self.power* self.steering)
            self.rf_motor.set(self.power*(2-self.steering))
            self.rr_motor.set(self.power*(2-self.steering))
        if self.switch.get(): #If you press button to switch
            self.mode = 'arcade' if self.mode == 'tankdrive' else 'tankdrive'
            print('switched to ' + self.mode)

if __name__ == '__main__': #If it's called, Run the Sucker!
    wpilib.run(MyRobot)
