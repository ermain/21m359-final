from __future__ import division

#######################
# GLOVE GRAPHICS file #
#######################

import sys
sys.path.append('../common')
from core import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock

import random
import numpy as np
import bisect
from collections import namedtuple

# GloveInfo
# shows info about the glove. for debugging purposes only.
kShowGlobalConstants = True # in case we only want to display variables strictly
                            # related to the glove only

class GloveInfo(Widget):
  def __init__(self, glove_input, audio = None):
    super(GloveInfo, self).__init__()
    self.label = Label(text = 'foo', pos = self.pos, size = (150, 400),\
        valign='top', font_size='20sp')
    self.add_widget(self.label)
    self.glove_input = glove_input
    self.audio = audio
    self.text = None

  # set text line for debugging
  def set_text(self, text, val = None):
    self.text = text
    if val is not None:
      self.text += "%f \n" % val

  def on_update(self):
    self.label.text = "fps: %f \n" % kivyClock.get_fps()
    if self.audio is not None:
      self.label.text += self.audio.get_load() + "\n"
    if self.text is not None:
      self.label.text += self.text
    finger_vals = self.glove_input.get_state()
    self.label.text += "finger state: %s \n" % " ".join(str(x) for x in finger_vals)

# note head of the notes display
class NoteHead(InstructionGroup):
  w = 40
  h = 30
  def __init__(self, pos, color):
    super(NoteHead, self).__init__()
    self.pos = pos
    self.color = Color(*color)
    self.add(self.color)
    self.head = Ellipse(segments = 40, angle_start = 0, angle_end = 15)
    self.head.pos = self.pos
    self.head.size = (self.w, self.h)

  def set_pos(self, pos):
    self.pos = pos
    self.head.pos = pos

  def set_color(self, color):
    self.color = Color(*color)

  def show(self):
    self.add(self.head)

  def hide(self):
    self.remove(self.head)

# collects all the note heads into a display
class NoteDisplay(InstructionGroup):
  def __init__(self, pos, callback):
    super(NoteDisplay, self).__init__()

  def scroll(self, dx):
    pass

  def on_update(self, dt):
    pass

