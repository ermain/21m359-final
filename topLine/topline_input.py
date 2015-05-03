import random
import numpy as np
import sys
import math
sys.path.append('./common')
from kinect import *
import time
class ToplineInput(object):
  def __init__(self, songPlayer, display_callback):
    #if using_kinect:
    #  self.topline = KinectTopLine(audio_callback, display_callback, scroller_callback)
    #else:
    #  self.topline = ScreenTopLine(audio_callback, display_callback, scroller_callback)

    self.songPlayer = songPlayer
    self.display_callback = display_callback
   
    self.settingsMode = False

    self.joint = None

    self.calibratedHeadHeight = 0.5

  def calibrateHeadHeight(self):
    totalTime = 0
    headHeights = 0 
    cnt = 0
    time.sleep(3)
    while totalTime < 2:
      self.kinect.on_update() 
      pt = self.kinect.get_joint(self.joint)
      pt_min = np.array([-1000.0, -1000, 0])
      pt_max = np.array([1000.0, 1000, 2000])
      norm_pt = scale_point(pt, pt_min, pt_max)
      headHeights += norm_pt[1]
      cnt += 1.
      time.sleep(0.01)
      totalTime += 0.01
    self.calibratedHeadHeight = headHeights / cnt
    print "CALIBRATED HEAD HEIGHT", self.calibratedHeadHeight

  def on_update(self,pt):
    self.topline.on_update(pt)

  def updatePosition(self, pt, pt_min, pt_max):
    
    norm_pt = scale_point(pt, pt_min, pt_max)

    if self.joint == kJointHead:
      scaled = scaledX(norm_pt[1], self.calibratedHeadHeight-0.1, self.calibratedHeadHeight+0.1, 0., 1)
      #print norm_pt[1], avgY, scaled

      gain = min(1,max(0.01,scaled))
    else:
      #gain = min(1,max(0.01,(norm_pt[1] - 0.3) / .4))
      gain = norm_pt[1]
    self.songPlayer.updateGain(gain)

    self.display_callback.set_pos(norm_pt)
    if not self.settingsMode: 
      if self.nextNoteCueOnLeft and norm_pt[0] < 0.5:
        self.nextNoteCueOnLeft = False
      elif self.nextNoteCueOnLeft == False and norm_pt[0] > 0.5:
        self.nextNoteCueOnLeft = True
      else:
        return
      self.songPlayer.playNextNote()
      self.display_callback.note_hit()




  def pointInRangeOf(self, ptToTest, centralPoint, threshold):
    x1 = ptToTest[0]
    y1 = ptToTest[1]
    x2 = centralPoint[0]
    y2 = centralPoint[1]
    return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ) <= threshold

class KinectTopLine(ToplineInput):
  def __init__(self, songPlayer, display_callback):
    ToplineInput.__init__(self, songPlayer, display_callback)
    #self.songPlayer = songPlayer
    #self.display_callback = display_callback
    #self.scroller_callback = scroller_callback

    self.nextNoteCueOnLeft = True
    self.joint = kJointHead #kJointHead 
    self.kinect = Kinect()
    self.kinect.add_joint(self.joint)
    self.tempJoint = None

  def toPlayMode(self):
    self.settingsMode = False
    self.update_joint()

  def toSettingsMode(self):
    self.settingsMode = True

    self.kinect.remove_joint(self.joint)
    self.joint = kJointRightHand
    self.kinect.add_joint(kJointRightHand)

  def update_joint(self):
    if self.tempJoint and self.tempJoint != self.joint:
      self.kinect.remove_joint(self.joint)

      self.kinect.add_joint(self.tempJoint)
      self.joint = self.tempJoint
      if self.joint == kJointHead:
        self.calibrateHeadHeight()


  def checkForSettingsCue(self):
    head_pt = self.kinect.get_joint(self.joint)
    pt_min = np.array([-1000.0, -1000, 0])
    pt_max = np.array([1000.0, 1000, 2000])

    norm_pt = scale_point(head_pt, pt_min, pt_max)
    if norm_pt[0] > 0.7 and norm_pt[0] > 0.7:
      return True
    return False 

  def on_update(self,pt):
    self.kinect.on_update()

    pt = self.kinect.get_joint(self.joint)
    pt_min = np.array([-1000.0, -1000, 0])
    pt_max = np.array([1000.0, 1000, 2000])
    norm_pt = scale_point(pt, pt_min, pt_max)
    self.updatePosition(pt, pt_min, pt_max)

    if self.settingsMode:
      self.checkIfInJointRegion(norm_pt)

  def checkIfInJointRegion(self, pt):
    if self.pointInRangeOf(pt, (0.62, 0.49), 0.05):
      self.display_callback.updateKinectSelection( (491,295))
      self.tempJoint = kJointRightHand
    elif self.pointInRangeOf(pt, (0.36, 0.49), 0.05):
      self.display_callback.updateKinectSelection((285.0, 292.0))
      self.tempJoint = kJointLeftHand
    elif self.pointInRangeOf(pt, (0.48, 0.80), 0.05):
      self.display_callback.updateKinectSelection((387.0, 502.0))
      self.tempJoint = kJointHead


def scaledX(x, min_val, max_val, a, b):
   return a + ((b-a)*(x-min_val)) / (max_val - min_val)


class ScreenTopLine(ToplineInput):
  def __init__(self, songPlayer, display_callback):
    ToplineInput.__init__(self, songPlayer, display_callback)

    self.nextNoteCueOnLeft = True

  def on_update(self, pt):
    pt_min = np.array([0., 0., 0.])
    pt_max = np.array([800., 600., 1.])

    self.updatePosition(pt, pt_min, pt_max)

  def toPlayMode(self):
    self.settingsMode = False

# convert pt into unit scale (ie, range [0,1]) assuming that pt falls in the
# the range [min_val, max_val]
# value is clipped [0,1]
def scale_point(pt, min_val, max_val):
   pt = (pt - np.array(min_val)) / (np.array(max_val) - np.array(min_val))
   pt = np.clip(pt, 0, 1)
   return pt
