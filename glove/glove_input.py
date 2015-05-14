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
from kivy.clock import Clock as kivyClock

class GloveInput(object):
  def __init__(self, audio_callback, display_callback, scroller_callback, using_real_glove = False):
    super(GloveInput, self).__init__()
    self.is_real_glove = using_real_glove
    if using_real_glove:
      self.glove = HandGlove(audio_callback, display_callback, scroller_callback)
    else:
      self.glove = KeyboardGlove(audio_callback, display_callback, scroller_callback)

  def on_button_down(self, keycode):
    self.glove.on_button_down(keycode)

  def on_button_up(self, keycode):
    self.glove.on_button_up(keycode)

  def on_update(self, dt):
    self.glove.on_update(dt)

  def get_state(self):
    return self.glove.state
  
  def disable(self):
    if self.is_real_glove:
      self.glove.disable()

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
  def on_update(self, dt):
    pass

class HandGlove(object):
  finger_threshholds = [0.8, 0.8, 0.8, 0.9, 0.8]
  max_line_size = 100
  port = '/dev/tty.usbserial-AH00SBIQ' # '/dev/tty.HC-06-DevB'
  max_val = 570
  min_val = 250
  debounce = 0.1

  def __init__(self, audio_callback, visual_callback, scroller_callback):
    super(HandGlove, self).__init__()
    # set up serial
    print "setting up serial..."
    try:
      self.ser = serial.Serial(\
            port=self.port,\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            timeout=1,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS)
      print "opened port ", self.port
      self.ser.flushInput()
      self.ser.flushOutput()
    except serial.SerialException:
      print "cannot open port ", self.port, "error: ", sys.exc_info()[0]
    except:
      print "unexpected error:", sys.exc_info()[0]
    self.audio_callback = audio_callback
    self.visual_callback = visual_callback
    self.scroller_callback = scroller_callback
    self.state = [False,False,False,False,False]
    print "after setting up serial"
    self.first_update = True

    #prevent lots of notes from being played at once
    self.debounce_timer = self.debounce

  def on_update(self, dt):
    if self.first_update:
      self.first_update = False
      self.ser.flushInput()
    else:
      data_str = self.ser.readline()
      if self.debounce_timer > 0:
        self.debounce_timer -= dt
      else:
        self.state = self.parse_data(data_str)

  def parse_data(self, data_str):
    data = data_str.split()
    fingers_down = []
    already_pressed = False
    idx = 0
    for d in data[:5]:
      state = (int(d) - self.min_val)/(self.max_val - self.min_val)
      if state < self.finger_threshholds[idx] and not already_pressed:
        fingers_down.append(True)
        if not self.state[idx]:
          self.on_finger_down(idx) # the finger pressed
        already_pressed = True
      else:
        fingers_down.append(False)
      idx += 1
    # if we've changed states, start up debounce timer.
    if fingers_down != self.state:
      self.debounce_timer = self.debounce
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
