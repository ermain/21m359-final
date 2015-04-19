

# common import
import sys
sys.path.append('./common')
from core import *
from graphics import *
from synth import *
from audio import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock

import random
import numpy as np


class GlassGraphics(InstructionGroup):
  def __init__(self):
      super(GlassGraphics, self).__init__()
      self.line = Triangle(points=[100,100,100,300,400,200], width=2)
      self.add(self.line)

class SongPlayer(object):
   def __init__(self, notePlayer):
      super(SongPlayer, self).__init__()

      self.song = [ (50,50), (51,50), (53,50) ]

      self.indexInSong = 0
      self.notePlayer = notePlayer

   def playNextNote(self):
      nextPitch, nextDuration = self.song[self.indexInSong]
      self.notePlayer.play_note(nextPitch, 100, nextDuration)
      self.indexInSong += 1

class NotePlayer(object):
   def __init__(self, synth, channel):
      super(NotePlayer, self).__init__()
      self.synth = synth
      self.timeElapsed = 0
      self.notesBeingPlayed = []
      self.channel = channel

   def play_note(self, pitch, velocity, duration):
      self.synth.noteon(self.channel, pitch, velocity) 
      self.notesBeingPlayed.append( (pitch, self.timeElapsed + duration))

   def on_update(self, dt):
      self.timeElapsed += dt
      notesBeingPlayedCopy = []
      for pitch, cuttoffTime in self.notesBeingPlayed:
         if cuttoffTime <= self.timeElapsed:
            self.synth.noteoff(self.channel, pitch)
         else:
            notesBeingPlayedCopy.append( (pitch, cuttoffTime))
      self.notesBeingPlayed = notesBeingPlayedCopy

class MainWidget(BaseWidget) :
   def __init__(self):
      super(MainWidget, self).__init__()
  
      self.audio = Audio()
      self.synth = Synth('common/FluidR3_GM.sf2')
      self.synth.program(0, 0, 41) #viola
      self.audio.add_generator(self.synth)
      #self.synth.noteon(0, 50, 25) 

      self.notePlayer = NotePlayer(self.synth,0)
      self.songPlayer = SongPlayer(self.notePlayer)

      self.glassGraphics = GlassGraphics()
      self.canvas.add(self.glassGraphics)
   def on_key_down(self, keycode, modifiers):
      if keycode[1] == '1':
         self.songPlayer.playNextNote()
         
      if keycode[1] == 'up':
         print self.audio.get_gain()
         self.audio.set_gain(self.audio.get_gain()*1.2)

      if keycode[1] == 'down':
         print self.audio.get_gain()
         self.audio.set_gain(self.audio.get_gain()*0.8)
   # handles changes to mode and strings
   def on_update(self) :
      dt = kivyClock.frametime
      self.notePlayer.on_update(dt)

# pass in which MainWidget to run as a command-line arg
run(MainWidget)
