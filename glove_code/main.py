from __future__ import division

import sys
sys.path.append('./common')
from core import *
from audio import *
from synth import *
from arduino import *
from player import *

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock as kivyClock

class MainWidget(BaseWidget):
  def __init__(self):
    super(MainWidget, self).__init__()
    self.label = Label(text = 'foo', pos = (50, 300), size = (400, 200), \
        valign='top', font_size='12sp')
    self.add_widget(self.label)
 
    self.arduino = Arduino()
    
    self.audio = Audio()
    self.synth = Synth('FluidR3_GM.sf2')
    self.audio.add_generator(self.synth)

    chan_settings = [(0, 0, 1),(1, 0, 2), (2, 0, 2), (3, 0, 3)]
    self.notes = [(60, 127, 1), (64, 127, 1), (67, 127, 1), (72, 127, 1)]
    self.note_player = NotePlayer(self.synth, chan_settings)
    
    self.finger_state = [False, False, False, False]

  def on_key_down(self, keycode, modifiers):
    if keycode[1] == 'spacebar':
      for f_idx in range(len(self.finger_state)):
        if self.finger_state[f_idx]:
          n = self.notes[f_idx]
          self.note_player.play_note(n[0], n[1], n[2], f_idx)

  def on_update(self):
    # update notes
    self.note_player.on_update(kivyClock.frametime)

    # update finger values
    finger_vals = self.arduino.on_update()
    self.label.text = "Finger Values: \n"
    self.label.text += " ".join(str(x) for x in finger_vals) + "\n"
    if len(finger_vals) == 4:
      for f_idx in range(len(finger_vals)):
        if finger_vals[f_idx]:
          self.finger_state[f_idx] = True
        else:
          self.finger_state[f_idx] = False
    
run(MainWidget)
