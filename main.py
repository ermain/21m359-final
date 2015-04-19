# common import
import sys
sys.path.append('./common')
from core import *
from graphics import *
from synth import *
from audio import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle, Bezier
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock

import random
import numpy as np


# Glass line
Y = 200
HEIGHT = 100
START_X = 600
END_X = 100


class GlassGraphics(InstructionGroup):
   def __init__(self):
      super(GlassGraphics, self).__init__()
      self.activeFigures = []
      self.elapsedTime = 0

   def drawFigure(self, gain):
      points=[START_X,Y+gain*100, START_X+10,Y+gain*100]
      figure = Line(points=points)
      self.add(figure)
      self.activeFigures.append(figure)

   def on_update(self,dt, gain):
      self.elapsedTime += dt
      figures = []
      if self.elapsedTime > 0:
         self.elapsedTime = 0
         for figure in self.activeFigures:
            newPoints = []
            for index in range(0,len(figure.points)):

               if index % 2 == 0: # even, thus x-indecis
                  if figure.points[index] > END_X:
                     newPoints.append(figure.points[index] - 1)
               else:
                  if figure.points[index-1] > END_X:
                     newPoints.append(figure.points[index])
            newPoints.append(newPoints[-2]+1)
            newPoints.append(Y+gain*100)
            self.remove(figure)
            print newPoints
            figure = Line(
                    points=newPoints,
                    segments=150,
                    loop=False)
            self.add(figure)   
            
            figures.append(figure)
         self.activeFigures = figures


            #figure.pos = (figure.pos[0] - 10, figure.pos[1])
      '''
      figures = []
      for figure in self.activeFigures:
         print figure.points
         if figure.points[0] < END_X:
            self.remove(figure)
         else:
            for index in range(0,len(figure.points)):
               if index % 2 == 0: # even, thus x-indecis
                  figure.points[index] = figure.points[index] - 10
            #figure.points.append(figure.points[-2]+1)
            #figure.points.append(Y)
            #figure.size = (figure.size[0], figure.size[0]*gain)
            figures.append(figure)
      self.activeFigures = figures
      '''
class SongPlayer(object):
   def __init__(self, notePlayer):
      super(SongPlayer, self).__init__()
      self.song = [ (64,4), (65,4), (67,3), (62,1), (64,3) ]
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
      self.previousPitch = None
      self.channel = channel

   def play_note(self, pitch, velocity, duration):
      if self.previousPitch:
         self.synth.noteoff(self.channel, self.previousPitch)
      self.synth.noteon(self.channel, pitch, velocity) 
      self.previousPitch = pitch
      #self.notesBeingPlayed.append( (pitch, self.timeElapsed + duration))

   '''
   def on_update(self, dt):
      self.timeElapsed += dt
      notesBeingPlayedCopy = []
      for pitch, cuttoffTime in self.notesBeingPlayed:
         if cuttoffTime <= self.timeElapsed:
            self.synth.noteoff(self.channel, pitch)
         else:
            notesBeingPlayedCopy.append( (pitch, cuttoffTime))
      self.notesBeingPlayed = notesBeingPlayedCopy
   '''

class MainWidget(BaseWidget) :
   def __init__(self):
      super(MainWidget, self).__init__()
  
      self.audio = Audio()
      self.synth = Synth('common/FluidR3_GM.sf2')
      self.synth.program(0, 0, 40) #violin
      self.audio.add_generator(self.synth)
      #self.synth.noteon(0, 50, 25) 

      self.notePlayer = NotePlayer(self.synth,0)
      self.songPlayer = SongPlayer(self.notePlayer)

      self.glassGraphics = GlassGraphics()
      self.canvas.add(self.glassGraphics)

   def on_key_down(self, keycode, modifiers):
      if keycode[1] == '1':
         self.songPlayer.playNextNote()
         self.glassGraphics.drawFigure(self.audio.get_gain())
      if keycode[1] == 'up':
         print self.audio.get_gain()
         self.audio.set_gain(min(1,self.audio.get_gain()+0.05))

      if keycode[1] == 'down':
         print self.audio.get_gain()
         self.audio.set_gain(max(0.01,self.audio.get_gain()-0.05))

   # handles changes to mode and strings
   def on_update(self) :
      dt = kivyClock.frametime
      #self.notePlayer.on_update(dt)
      self.glassGraphics.on_update(dt, self.audio.get_gain())

# pass in which MainWidget to run as a command-line arg
run(MainWidget)
