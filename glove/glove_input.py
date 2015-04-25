from __future__ import division

####################
# GLOVE INPUT file #
####################

import sys
sys.path.append('../common')
from core import *

import random
import numpy as np
import bisect
import serial
from collections import namedtuple


class GloveInput(object):
  def __init__(self, audio_callback, display_callback, scroller_callback, using_real_glove = False):
    super(GloveInput, self).__init__()
    if using_real_glove:
      self.glove = HandGlove(audio_callback, display_callback, scroller_callback)
    else:
      self.glove = KeyboardGlove(audio_callback, display_callback, scroller_callback)

  def on_button_down(self, keycode):
    self.glove.on_button_down(keycode)

  def on_button_up(self, keycode):
    self.glove.on_button_up(keycode)

  def on_update(self):
    self.glove.on_update()

  def get_state(self):
    return self.glove.state

class KeyboardGlove(object):
  keys = "12345"
  def __init__(self, audio_callback, visual_callback, scroller_callback):
    super(KeyboardGlove, self).__init__()
    self.audio_callback = audio_callback
    self.visual_callback = visual_callback
    self.scroller_callback = scroller_callback
    self.state = [False, False, False, False, False]

  def on_finger_down(self, lane):
    if self.audio_callback:
      self.audio_callback(lane)
    if self.visual_callback:
      self.visual_callback(lane)
    if self.scroller_callback:
      self.scroller_callback()
  
  def on_button_down(self, keycode):
    if keycode[1] in self.keys:
      idx = int(keycode[1]) - 1
      self.state[idx] = True
      self.on_finger_down(idx)

  def on_button_up(self, keycode):
    if keycode[1] in self.keys:
      self.state[int(keycode[1]) - 1] = False
       
  # don't need to do anything
  def on_update(self):
    pass

class HandGlove(object):
  finger_thres = 0.6
  max_line_size = 100
  port = '/dev/tty.HC-06-DevB'
  max_val = 570
  min_val = 250

  def __init__(self, audio_callback, visual_callback, scroller_callback):
    super(Glove, self).__init__()
    # set up serial
    self.ser = serial.Serial(\
          port=self.port,\
          baudrate=9600,\
          parity=serial.PARITY_NONE,\
          timeout=10,\
          stopbits=serial.STOPBITS_ONE,\
          bytesize=serial.EIGHTBITS)
    self.audio_callback = audio_callback
    self.visual_callback = visual_callback
    self.scroller_callback = scroller_callback
    self.state = [False,False,False,False,False]
  
  def on_update(self):
    data_str = self.ser.readline()
    self.state = self.parse_data(data_str)

  def parse_data(self, data_str):
    data = data_str.split()
    fingers_down = []
    for d in data[:4]:
      state = (int(d) - self.min_val)/(self.max_val - self.min_val)
      if state < self.finger_thres:
        fingers_down.append(True)
        on_finger_down(len(fingers_down) - 1) # the finger pressed

      else:
        fingers_down.append(False)
    return fingers_down

  def disable(self):
    self.ser.close()

  def enable(self):
    self.ser.open()
 
  def on_finger_down(self, lane):
    if self.audio_callback:
      self.audio_callback(lane)
    if self.visual_callback:
      self.visual_callback(lane)
    if self.scroller_callback:
      self.scroller_callback()

  def on_button_down(self, keycode):
    pass

  def on_button_up(self, keycode):
    pass
