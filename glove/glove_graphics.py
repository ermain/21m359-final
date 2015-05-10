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
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate, Mesh
from kivy.clock import Clock as kivyClock
from kivy.core.image import Image

import random
import numpy as np
import bisect
from collections import namedtuple

sys.path.append('./topLine')
from readFile import *

# GloveInfo
# shows info about the glove. for debugging purposes only.
kShowGlobalConstants = True # in case we only want to display variables strictly
                            # related to the glove only
class GloveDisplayData(object):
  def __init__(self, filepath):
    self.notes = []
    self._read_in_data(filepath)

  def _read_in_data(self, filepath):
    # make a dictionary mapping notes in topline to their
    # duration, where 1 = a quarter note
    # this is used in GloveNoteHead to display a notehead for the
    # solo lines above the 
    songData = parseSong()
    soloLineMap = {}
    counter = 0
    for x in songData.songElements:
      soloLineMap[counter] = x
      counter += float(x.duration)

    num_gems = 0
    with open(filepath) as f:
      counter = 0
      for line in f.readlines():
        if ":" in line:
          len, pattern = line.split(":")

          len = 1/int(len) * 4 

          for n in pattern:
            if n in "12345":
              if counter in soloLineMap.keys():
                soloNote = soloLineMap[counter]
              else:
                soloNote = False
              self.notes.append((int(n)-1, len, soloNote))
            counter += len


  def get_at_idx(self, idx):
    return self.notes[idx]

  def get_all_notes(self):
    return self.notes


class GloveInfo(Widget):
  def __init__(self, glove_input, audio = None):
    super(GloveInfo, self).__init__()
    self.label = Label(text = 'foo', pos = (100,100), size = (150, 400),\
        valign='top', font_size='12sp')
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


class ToplineNoteHead(InstructionGroup):
  def __init__(self, pos, duration, future_color, past_color, spacing_per_lane, locationInSong):
    super(ToplineNoteHead, self).__init__()
    self.pos = pos
    self.duration = float(duration)
    self.spacing_per_lane = spacing_per_lane

    self.future_color = future_color
    self.past_color = past_color
    self.color = Color(*future_color)
    self.add(self.color)

    self.noteHead = Rectangle(pos=self.pos, size=(self.duration*(self.spacing_per_lane+4)*5, 50))
    self.add(self.noteHead)

    self.locationInSong = locationInSong

  def set_lane(self, lane):
    self.pos = (self.base_pos[0], self.base_pos[1] )
    #self.circle.pos = (self.pos[0] - self.w, self.pos[1] - self.w)

  def set_color_future(self):
    self.color.r = self.future_color[0]
    self.color.g = self.future_color[1]
    self.color.b = self.future_color[2]

  def set_color_past(self):
    self.color.r = self.past_color[0]
    self.color.g = self.past_color[1]
    self.color.b = self.past_color[2]

  def set_color(self, color):
    self.color = Color(*color)

  def show(self):
    self.add(self.noteHead)

  def hide(self):
    self.remove(self.noteHead)

# note head of the notes display
class GloveNoteHead(InstructionGroup):
  w = 15
  h = 15

  def __init__(self, pos, lane, lane_spacing, future_color, past_color, texture):
    super(GloveNoteHead, self).__init__()
    self.base_pos = pos
    self.pos = (pos[0], pos[1] + lane*lane_spacing) 
    self.lane_spacing = lane_spacing
    self.future_color = future_color
    self.past_color = past_color
    self.color = Color(*future_color)
    self.add(self.color)
    """self.mesh = Mesh()
    self.mesh.indices = [0,1,2,3]
    self.mesh.vertices = [\
        self.pos[0] - self.w/2, self.pos[1] - self.h/2, 0, 0,\
        self.pos[0] - self.w/2, self.pos[1] + self.h/2, 0, 1,\
        self.pos[0] + self.w/2, self.pos[1] - self.h/2, 1, 0,\
        self.pos[0] + self.w/2, self.pos[1] + self.h/2, 1, 1\
        ]
    if texture:
      self.mesh.texture = Image(texture).texture
    self.mesh.mode = "triangle_strip"
    self.add(self.mesh)
  """
    self.circle = Rectangle(pos=self.pos)#Ellipse(segments = 5)
    self.circle.size = self.w*2, self.w*2
    self.circle.pos = (self.pos[0] , self.pos[1] - self.w)
    self.add(self.circle)

  def set_lane(self, lane):
    self.pos = (self.base_pos[0], self.base_pos[1] + lane*self.lane_spacing)
    self.circle.pos = (self.pos[0] , self.pos[1] - self.w)
  """  self.mesh.vertices = [\
        self.pos[0] - self.w/2, self.pos[1] - self.h/2, 0, 0,\
        self.pos[0] - self.w/2, self.pos[1] + self.h/2, 0, 1,\
        self.pos[0] + self.w/2, self.pos[1] - self.h/2, 1, 0,\
        self.pos[0] + self.w/2, self.pos[1] + self.h/2, 1, 1\
        ]"""

  def set_color_future(self):
    self.color.r = self.future_color[0]
    self.color.g = self.future_color[1]
    self.color.b = self.future_color[2]

  def set_color_past(self):
    self.color.r = self.past_color[0]
    self.color.g = self.past_color[1]
    self.color.b = self.past_color[2]

  def set_color(self, color):
    self.color = Color(*color)

  def show(self):
    self.add(self.head)

  def hide(self):
    self.remove(self.head)

# collects all the note heads into a display
class GloveNoteDisplay(InstructionGroup):
  spacing_per_quarter = 175
  spacing_per_lane = 30
  future_color = (149/255, 165/255, 166/255)
  past_color = (46/255, 204/255, 113/255)
  speed_factor = 0.25

  def __init__(self, pos, texture, data):
    super(GloveNoteDisplay, self).__init__()
    self.add(PushMatrix())
    self.data = data
    self.translate = Translate(0,0)
    self.add(self.translate)
    
    self.start_pos = pos
    cur_x = pos[0]
    self.note_heads = []

    self.topline_noteheads = []
    locationInSong = 0
    for n in data.get_all_notes():
      self.note_heads.append(GloveNoteHead((cur_x, pos[1]), n[0], self.spacing_per_lane, \
         self.future_color, self.past_color, texture))

      if n[2] != False:
        # add a notehead above the current notehead if there should be 
        # a top solo line note there

        g = ToplineNoteHead((cur_x, pos[1]+200), n[2].duration,  self.future_color, self.past_color, self.spacing_per_lane, locationInSong)
        if n[2].note != 'R':
          self.add(g)
        self.topline_noteheads.append(g)
        locationInSong += g.duration
        

      self.add(self.note_heads[-1])
      cur_x += n[1] * self.spacing_per_quarter
    
    self.x = 0
    self.target_x = 0
    self.next_note = 0
    self.next_topline_note = 0
    self.add(PopMatrix())


  def scroll(self, dx):
    #print "scrolling"
    self.target_x = self.target_x - dx

  def scroll_to_next_note(self):
    #print self.data.get_at_idx(self.next_note)[1]*self.spacing_per_quarter
    self.scroll(self.data.get_at_idx(self.next_note)[1]*self.spacing_per_quarter)

  def on_update(self, dt):
    if abs(self.x - self.target_x) > 0.01:
      self.x += (self.target_x - self.x) * self.speed_factor
      self.translate.x = self.x

  # should be passed to the input driver as a callback
  def on_note_hit(self, lane):
    self.note_heads[self.next_note].set_color_past()
    self.note_heads[self.next_note].set_lane(lane)
    self.next_note += 1


  def getTopLineNoteClosestToBottom(self):
    locationInSong = self.next_note*0.25
    for index, note in enumerate(self.topline_noteheads):
      if note.locationInSong + note.duration > locationInSong:
        return index

  def on_topline_note_hit(self):
    # change color of note
    
    notehead = self.topline_noteheads[self.next_topline_note]

    if abs(notehead.locationInSong - self.next_note*0.25) <= 2:
      notehead.set_color_past()
      noteIndexToPlay = self.next_topline_note
      self.next_topline_note += 1
      return noteIndexToPlay
    else:
      self.next_topline_note = self.getTopLineNoteClosestToBottom()
    return False
class Scroller(object):
  def __init__(self, glove_display):
    self.glove_display = glove_display
    
  def on_glove_hit(self):
    self.glove_display.scroll_to_next_note()
