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
    self.audio = Audio()
    self.synth = Synth("../common/FluidR3_GM.sf2")
    self.audio_data = GloveAudioData("prelude_notes.txt")
    self.audio_player = GloveAudioPlayer(self.audio_data, (0,0,0), self.synth, self.audio)
    
    self.note_data = GloveDisplayData("prelude_visuals.txt")
    glove_pos = (400, 300)
    self.note_display = GloveNoteDisplay(glove_pos, "circletexture.png", self.note_data)
    self.canvas.add(self.note_display)
    self.scroller = Scroller(self.note_display)

    self.input = GloveInput(self.audio_player.play_next_note, \
       self.note_display.on_note_hit, self.scroller.on_glove_hit, kUsingGlove)
    #self.input = GloveInput(self.audio_player.play_next_note, \
    #    None, kUsingGlove)
    self.info = GloveInfo(self.input, self.audio_player.audio)
    self.add_widget(self.info)

  def on_key_down(self, keycode, modifiers):
    self.input.on_button_down(keycode)

  def on_key_up(self, keycode):
    self.input.on_button_up(keycode)

  def on_update(self):
    dt = kivyClock.frametime
    self.audio_player.on_update(dt)
    self.input.on_update()
    self.info.on_update()
    self.note_display.on_update(dt)

run(GloveWidget)
