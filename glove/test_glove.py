from __future__ import division

###################
# GLOVE TEST file #
###################

import sys
sys.path.append('../common')
from core import *
from audio import *
from clock import *
from song import *
from wavegen import *

from glove_audio import *
from glove_graphics import *
from glove_input import *

import random
import numpy as np
import bisect
from collections import namedtuple
from kivy.clock import Clock as kivyClock

kUsingGlove = False

class GloveWidget(BaseWidget):
  def __init__(self):
    super(GloveWidget, self).__init__()
    self.audio_data = GloveAudioData("prelude.txt")
    self.audio_player = GloveAudioPlayer(self.audio_data, (0,0,0))
    self.input = GloveInput(self.audio_player.play_next_note, kUsingGlove)
    self.info = GloveInfo(self.input, self.audio_player.audio)
 
  def on_key_down(self, keycode, modifiers):
    self.input.on_button_down(keycode)

  def on_key_up(self, keycode):
    self.input.on_button_up(keycode)

  def on_update(self):
    dt = kivyClock.frametime
    self.audio_player.on_update(dt)
    self.input.on_update()
    self.info.on_update()

run(GloveWidget)
