_author_ = 'Darshan Kothari'

import os, sys, inspect #import os, sys, inspect to set Leap library
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe())) #set the src dir
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib')) #join the lib and src file
sys.path.insert(0, lib_dir)
import Leap # import Leap library from ../lib

#SubListener to help out with the Listener class in the Leap Library

class SubListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers),
                len(frame.tools), len(frame.gestures()))

        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            print " %s, id %d, position: %s" % (handType, hand.id, hand.palm_position)

            normal = hand.palm_normal
            direction = hand.direction

            print "pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % ( direction.pitch * Leap.RAD_TO_DEG,
                    normal.roll * Leap.RAD_TO_DEG,
                    direction.yaw * Leap.RAD_TO_DEG)
            arm = hand.arm
            print "Arm direction: %s, wrist postiion: %s, elbow position: %s" % ( arm.direction, arm.wrist_position, arm.elbow_position)

            for finger in hand.fingers:
                print "\t %s finger, id: %d, length: %fmm, width: %fmm" % (self.finger_names[finger.type()], finger.id, finger.length, finger.width)

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"
        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"
        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"
        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
def main():

        listener = SubListener()
        controller = Leap.Controller()

        controller.add_listener(listener)

        print "Press Enter to quit..."
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            controller.remove_listener(listener)


if __name__ == "__main__":
    main()







