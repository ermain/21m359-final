import random
import numpy as np
import sys
sys.path.append('./common')
from kinect import *
class ToplineInput(object):
  def __init__(self, audio_callback, display_callback, scroller_callback, using_kinect = False):
    if using_kinect:
      self.topline = KinectTopLine(audio_callback, display_callback, scroller_callback)
    else:
      self.topline = ScreenTopLine(audio_callback, display_callback, scroller_callback)

    self.audio_callback = audio_callback
    self.display_callback = display_callback
    self.scroller_callback = scroller_callback

  def on_update(self,pt):
    self.topline.on_update(pt)

  def updatePosition(self, norm_pt):
    self.display_callback.set_pos(norm_pt)
    if self.nextNoteCueOnLeft and norm_pt[0] < 0.5:
      self.nextNoteCueOnLeft = False
    elif self.nextNoteCueOnLeft == False and norm_pt[0] > 0.5:
      self.nextNoteCueOnLeft = True
    else:
      return
    self.songPlayer.playNextNote()
    self.display_callback.note_hit()

class KinectTopLine(ToplineInput):
  def __init__(self, songPlayer, display_callback, scroller_callback):
    self.songPlayer = songPlayer
    self.display_callback = display_callback
    self.scroller_callback = scroller_callback

    self.nextNoteCueOnLeft = True
    self.joint = kJointRightHand #kJointHead 
    self.kinect = Kinect()
    self.kinect.add_joint(self.joint)

  def on_update(self,pt):
    self.kinect.on_update()

    head_pt = self.kinect.get_joint(self.joint)
    pt_min = np.array([-1000.0, -1000, 0])
    pt_max = np.array([1000.0, 1000, 2000])

    norm_pt = scale_point(head_pt, pt_min, pt_max)
   # self.label.text = '\n'.join([str(x) for x in head_pt])

    gain = min(1,max(0.01,(norm_pt[1] - 0.3) / .4))
    self.songPlayer.updateGain(gain)
    super(KinectTopLine, self).updatePosition(norm_pt)

def scaledX(x, min_val, max_val, a, b):
   return a + ((b-a)*(x-min_val)) / (max_val - min_val)


class ScreenTopLine(ToplineInput):
  def __init__(self, songPlayer, display_callback, scroller_callback):
    self.songPlayer = songPlayer
    self.display_callback = display_callback
    self.scroller_callback = scroller_callback

    self.nextNoteCueOnLeft = True

  def on_update(self, pt):
    pt_min = np.array([0., 0., 0.])
    pt_max = np.array([800., 600., 1.])
    norm_pt = scale_point(pt, pt_min, pt_max)
    self.songPlayer.updateGain(norm_pt[1])
    super(ScreenTopLine, self).updatePosition(norm_pt)

# convert pt into unit scale (ie, range [0,1]) assuming that pt falls in the
# the range [min_val, max_val]
# value is clipped [0,1]
def scale_point(pt, min_val, max_val):
   pt = (pt - np.array(min_val)) / (np.array(max_val) - np.array(min_val))
   pt = np.clip(pt, 0, 1)
   return pt
