import wpilib #Import info on robot parts

from networktables import NetworkTable #Import stuff for the telop
from networktables.util import ntproperty

import math #It's math, dummy

#Constants
ENCODER_ROTATION = 1023
WHEEL_DIAMETER = 7.693
class Drive:
    """Drive communication with robutt goes through here"""


    sd = NetworkTable #I'm lazy, so I just want to write sd instead of NetworkTable

    def _init_(self): #Initialization of key info
        self.sd = NetworkTable.getTable('/SmartDashboard') #Set up conection with dashboard
        self.angle_P = self.sd.getAutoUpdateValue('Drive/Angle_P', 0.055) #Set all the key info to where the info is
        self.angle_I = self.se.getAutoUpdateValue('Drive/Angle_I', 0)
        self.drive_constant = self.sd.getAutoUpdateValue('Drive/Drive_Constant', .0001)
        self.rotate_max = self.sd.getAutoUpdateValue('Drive/Max Gyro Rotate Speed', .37)

        self.enabled = False #Sets enabled to false upon start
        self.align_angle = None #From start, not aligned on an angle
        self.align_print_timer = wpilib.Timer() #set print timer to the actual timer
        self.align_print_time.start() #Starts aligning print timer upon initialization

    def on_enable(self):
        """ (NOTE FOR BLAINE, ASK ABOUT THIS GREEN TEXT)
            Constructor.
            :param robotDrive: a `wpilib.RobotDrive` object
            :type rf_encoder: DriveEncoders()
            :type lf_encoder: DriveEncoders()
        """
        #one_time initialization hack
        if not self.enabled:
            nt = NetworkTable.getTable('componets/autoaim')
            nt.addTableListener(self._align_angle_updated, True, 'target_angle')

        self.isTheRobotBackwards = False #initializes the robot not being backwards as start
        self.iErr = 0 #ASK ABOUT iErr
        #set defaults
        self.y = 0
        self.rotation = 0
        self.squaredInputs = False #default, don't square inputs

        self.halfRotation = 1 #half a rotation is one-time


        #VERB functions
        #PREVENTS CONFLICTION WHEN MULTIPLE CALLERS IN A loop

        def _align_angle_updated(self, source, key, value, isNew):
            #store abs of where we want to go to
            self.align_angle = value + self.return_gyro_angle() #sets the align of angle to gyro's angle
            self.align_angle_nt = self.align_angle #Same thing, but copied to Network Table

        def move(self, y, rotation, squaredInputs=False): #Required info to move somewhere
            """
            :param x: The speed that the robot should drive in the X direction. 1 is right [-1.0..1.0]
            :param y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0]
            :param rotation:  The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]
            :param squaredInputs: If True, the x and y values will be squared, allowing for more gradual speed.
            """
            self.y = max(min(y, 1), -1)
            self.rotation = max(min(1.0, roation), -1)
            self.squaredInputs = squaredInputs
        def set_angle_constant(self, constant): #sets the constant to measure turning speed
            self.angle_constant = constant

        def _get_inches_to_ticks(self,inches): #translates inches into encoeder ticks

            gear_ratio = 50/12
            target_position = (gear_ratio * ENCODER_ROTATION * inches) / (math.pi*WHEEL_DIAMETER)
            return target_position

        def drive_distance(self, inches, max_speed=.9): #return drive_distance
            return self.encoder_drive(self._get_inches_to_ticks(inches), max_speed)

        def set_direction(self, direction): #reverse direction
            self.isTheRobotBackwards = bool(direction)

        def switch_direction(self): #reverse front and back
            self.isTheRobotBackwards = not self.isTheRobotBackwards

        def halveRotation(self): #half the rotation
            self.halfRotation = 0.5

        def normalRotation(self): #Set rotation to normal
            self.halfRotation = 1

        def execute(self): #Execute(order 66) everything; make the robutt drive_distance
            backwards = -1 if self.isTheRobotBackwards else 1

            if(self.isTheRobotBackwards):
                self.robot_drive.arcadeDrive(-self.y, -self.rotation / 2, self.squaredInputs)
            else:
                self.robot_drive.arcadeDrive(backwards * self.y, -self.rotation * self.halfRotation, self.squaredInputs) #Bringing it all together

            #Default, the robot doesn't move
            self.y = 0
            self.rotation = 0
