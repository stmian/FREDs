_author_ = 'Darshan Kothari'

#import os, sys, inspect to set Leap Library
import os, sys, inspect
#get the pwd (linux command) of the current directory and set it as the path
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
#get the src_dir set the lib_dir to the Leap Library and set it as part of the path
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
#set the sys.path to include both the src_dir and lib_dir
sys.path.insert(0, lib_dir)
#import the Leap library
import Leap
import time
import httplib
inFlight = False
change = False

#Callibration var for hovering position.
conn = httplib.HTTPConnection("192.168.1.201:3000")
callibration = True
counter = 0
pitch = 0
yaw = 0
roll = 0
wristPos_x = 0
wristPos_y = 0
wristPos_z = 0

#SubListener Class goes here
class HelpListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exit"

    def on_frame(self, controller):
        global inFlight, callibration, counter, conn
        frame = controller.frame()
        hands = frame.hands
        if len(hands) > 1:
            print "Please use one hand only"
        elif len(hands) == 0:
            if callibration == True:
                print "Please place one hand over the Leap for callibration"
            else:
                if inFlight == True:
                    print "Landing"
                    conn = httplib.HTTPConnection("192.168.1.201:3000")
                    conn.request("GET", "/land")
                    conn.close()
                    inFlight = False
                    callibration = True
                    counter = 0
                else:
                    print "No hands are detected"
        else:
            if callibration == True:
                self.callibration_Leap(self.parseHandData(hands[0]), self.parseArmData(hands[0].arm))
            else:
                self.findCommand(self.parseHandData(hands[0]), self.parseArmData(hands[0].arm))

    def callibration_Leap(self, hdata, adata):
        global callibration, counter, pitch, yaw, roll, wristPos_x, wristPos_y, wristPos_z
        if counter == 0:
            print "Callibrating"
            pitch = hdata['pitch']
            yaw = hdata['yaw']
            roll = hdata['roll']
            wristPos_x = adata['x']
            wristPos_y = adata['y']
            wristPos_z = adata['z']
            counter += 1
        else:
            if counter == 500:
                print "callibration done"
                callibration = False
            counter += 1
            pitch = (pitch + hdata['pitch'])/2
            yaw = (yaw + hdata['yaw'])/2
            roll = (roll + hdata['roll'])/2
            wristPos_x = (wristPos_x + adata['x'])/2
            wristPos_y = (wristPos_y + adata['y'])/2
            wristPos_z = (wristPos_z + adata['z'])/2

    def findCommand(self, hdata, adata):
            #find the commmand to send to UV
            global inFlight, client, conn
            url = "192.168.1.2"
            if self.checkHovering(hdata, adata) and inFlight == False:
                self.toggleInFlight()
            else:
                if not self.checkHovering(hdata, adata) and inFlight == True:
                    if self.checkTurningLeft(hdata, adata):
                        print "Moving Left"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/ml")
                        conn.close()
                    elif self.checkTurningRight(hdata, adata):
                        print "Moving Right"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/mr")
                        conn.close()
                    elif self.checkFalling(hdata, adata):
                        print "Diving"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/f")
                        conn.close()
                    elif self.checkRising(hdata, adata):
                        print "Rising"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/b")
                        conn.close()
                    elif self.checkRotatingLeft(hdata, adata):
                        print "Rotating Left"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/tl")
                        conn.close()
                    elif self.checkRotatingRight(hdata, adata):
                        print "Rotating Right"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/tr")
                        conn.close()
                    else:
                        print "Do not Understand, hence Hovering"
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/stop")
                        conn.close()
                else:
                    if inFlight == True:
                        conn = httplib.HTTPConnection("192.168.1.201:3000")
                        conn.request("GET", "/stop")
                        conn.close()
                        print "Hovering"
                    else:
                        print "Please place hand in hovering mode"

    def checkPitchWithCallabration(self, data, bounds):
        bool_upper = data < bounds + 15
        bool_lower = data > bounds - 15
        return [bool_upper, bool_lower]

    def checkRollWithCallabration(self, data, bounds):
        bool_upper = data < bounds + 15
        bool_lower = data > bounds - 15
        return [bool_upper, bool_lower]

    def checkYawWithCallabration(self, data, bounds):
        bool_upper = data < bounds + 15
        bool_lower = data > bounds - 15
        return [bool_upper, bool_lower]

    def checkWristPosition_XYZ(self, data, bounds):
        bool_upper = data < bounds + 100
        bool_lower = data > bounds - 100
        return [bool_upper, bool_lower]

    def checkHovering(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = ((pitch_bool[0] == pitch_bool[1]) and (roll_bool[0] == roll_bool[1]) and (yaw_bool[0] == yaw_bool[1]))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def checkTurningRight(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = ((pitch_bool[0] == pitch_bool[1]) and ((roll_bool[0] == True) and  (roll_bool[1] == False)) and (yaw_bool[0] == yaw_bool[1]))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def checkTurningLeft(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = ((pitch_bool[0] == pitch_bool[1]) and ((roll_bool[0] == False) and  (roll_bool[1] == True)) and (yaw_bool[0] == yaw_bool[1]))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def checkRotatingLeft(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = ((pitch_bool[0] == pitch_bool[1]) and (roll_bool[0] == roll_bool[1]) and ((yaw_bool[0] == True) and  (yaw_bool[1] == False)))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def checkRotatingRight(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = ((pitch_bool[0] == pitch_bool[1]) and (roll_bool[0] == roll_bool[1]) and ((yaw_bool[0] == False) and  (yaw_bool[1] == True)))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def checkRising(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = (((pitch_bool[0] == False) and  (pitch_bool[1]== True)) and (roll_bool[0] == roll_bool[1]) and (yaw_bool[0] == yaw_bool[1]))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def checkFalling(self, hdata, adata):
        global pitch, roll, yaw, wristPos_x, wristPos_y, wristPos_z
        pitch_bool = self.checkPitchWithCallabration(hdata['pitch'], pitch)
        roll_bool = self.checkRollWithCallabration(hdata['roll'], roll)
        yaw_bool = self.checkYawWithCallabration(hdata['yaw'], yaw)
        wristPos_boolx = self.checkWristPosition_XYZ(adata['x'], wristPos_x)
        wristPos_booly = self.checkWristPosition_XYZ(adata['y'], wristPos_y)
        wristPos_boolz = self.checkWristPosition_XYZ(adata['z'], wristPos_z)
        hand_bool = (((pitch_bool[0] == True) and  (pitch_bool[1]== False)) and (roll_bool[0] == roll_bool[1]) and (yaw_bool[0] == yaw_bool[1]))
        wristPos_bool = ((wristPos_boolx[0] == wristPos_boolx[1]) and (wristPos_booly[0] == wristPos_booly[1]) and (wristPos_boolz[0] == wristPos_boolz[1]))
        return (hand_bool and wristPos_bool)

    def parseHandData(self, hand):
        rtodg = Leap.RAD_TO_DEG
        normal = hand.palm_normal
        direction = hand.direction
        pitch = direction.pitch * rtodg
        roll = normal.roll * rtodg
        yaw = direction.yaw * rtodg
        hand_data = {'pitch': pitch, 'roll': roll, 'yaw': yaw}
        return hand_data

    def parseArmData(self, arm):
        x = arm.wrist_position[0]
        y = arm.wrist_position[1]
        z = arm.wrist_position[2]
        return {'x': x, 'y': y, 'z': z}

    def toggleInFlight(self):
        global inFlight, conn
        if inFlight == False:
            print "Starting to Fly"
            url = "192.168.1.2"
            print url+"/takeoff"
            inFlight = True
            conn = httplib.HTTPConnection("192.168.1.201:3000")
            conn.request("GET", "/takeoff")
            conn.close()


def main():
    #initialize Listener Helper here before retrieving controller object
    listener = HelpListener()
    # get the Controller object of Leap
    controller = Leap.Controller()

    #add the listener to the controller object
    controller.add_listener(listener)

    #temporary exiting process
    print "Press any Key to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
