# common import
import sys
sys.path.append('./common')
from core import *
from graphics import *
from synth import *
from audio import *
from kinect import *

sys.path.append('./glove')
from glove_audio import *
from glove_graphics import *
from glove_input import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle, Bezier
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock


#from firebase import firebase



import random
import numpy as np

import readFile
# Glass line
Y = 200
HEIGHT = 100
START_X = 600
END_X = 100

kUseKinect = False 
joint = kJointRightHand

kUseGlass = False
# https://www.youtube.com/watch?v=FZ-HETHWLr0

class SongPlayer(object):
   def __init__(self, notePlayer):
      super(SongPlayer, self).__init__()

      self.song = readFile.parseSong().songElements
      self.indexInSong = 0
      self.notePlayer = notePlayer

   def playNextNote(self):
      songElement = self.song[self.indexInSong]
      pitch = songElement.midiNumber
      duration = songElement.duration
      dynamics = songElement.dynamics
      if pitch != None:
         print pitch
         self.notePlayer.play_note(pitch, 100, duration)
      else:
         self.notePlayer.stop_note()
      self.indexInSong += 1

class NotePlayer(object):
   def __init__(self, synth, channel):
      super(NotePlayer, self).__init__()
      self.synth = synth
      self.timeElapsed = 0
      self.previousPitch = None
      self.channel = channel


   def stop_note(self):
      if self.previousPitch:
         self.synth.noteoff(self.channel, self.previousPitch)

   def play_note(self, pitch, velocity, duration):
      if self.previousPitch:
         self.synth.noteoff(self.channel, self.previousPitch)
      self.synth.noteon(self.channel, pitch, velocity) 
      self.previousPitch = pitch
  

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

      #self.glassGraphics = GlassGraphics()
      #self.canvas.add(self.glassGraphics)

      self.nextNoteCueOnLeft =  True
      self.start = False

      if kUseKinect:
         self.kinect = Kinect()
         self.kinect.add_joint(joint)

      self.head = Cursor3D((800,600), (10, 10), (.2, .6, .2), True)
      self.canvas.add(self.head)

      self.line = Line(points=[400,0,400,600])
      self.canvas.add(self.line)


      #self.firebase = firebase.FirebaseApplication('https://glassinstrument.firebaseio.com', None)
      
      self.timeSinceLastNoteTriggered = 0

      self.label = Label(text = 'foo', pos = (50, 400), size = (150, 200), valign='top',
                         font_size='20sp')
      self.add_widget(self.label)

      self.gainLabel = Label(text = 'foo', pos = (50, 300), size = (150, 200), valign='top',
                         font_size='20sp')
      self.add_widget(self.gainLabel)
   
      # start glovestuff
      self.glove_audio_data = GloveAudioData("./glove/prelude_notes.txt")
      print "after data"
      self.glove_audio_player = GloveAudioPlayer(self.glove_audio_data, (1,0,0), \
         self.synth, self.audio) 
      print "after audio" 
      self.glove_input = GloveInput(self.glove_audio_player.play_next_note, \
          None, False)
      self.glove_info = GloveInfo(self.glove_input, self.glove_audio_player.audio)
      self.add_widget(self.glove_info)
      # end glovestuff

      self.start = True

   def on_key_down(self, keycode, modifiers):
      self.glove_input.on_button_down(keycode)
      
   def on_key_up(self, keycode):
      self.glove_input.on_button_up(keycode)

   # handles changes to mode and strings
   def on_update(self) :
      
      dt = kivyClock.frametime
      
      # start glovestuff
      self.glove_audio_player.on_update(dt)
      self.glove_input.on_update()
      self.glove_info.on_update()
      # end glovestuff

      #self.notePlayer.on_update(dt)
      #self.glassGraphics.on_update(dt, self.audio.get_gain())
      if self.start:
         if kUseGlass:
            self.timeSinceLastNoteTriggered += dt
            acc = self.firebase.get('/accData/accX', None)
            if self.nextNoteCueOnLeft and acc > 0.3 and self.timeSinceLastNoteTriggered > 0.1: 
               self.songPlayer.playNextNote()
               self.nextNoteCueOnLeft = False
               #self.audio.set_gain(norm_pt[1])
               self.timeSinceLastNoteTriggered = 0
            elif self.nextNoteCueOnLeft == False and acc < -0.3 and self.timeSinceLastNoteTriggered > 0.1:
               self.songPlayer.playNextNote()
               self.nextNoteCueOnLeft = True
               self.timeSinceLastNoteTriggered = 0
         elif kUseKinect == False:

            pt = [Window.mouse_pos[0], Window.mouse_pos[1], 0]
            if 'shift' in self.down_keys:
               pt[2] = 0.5

            pt_min = np.array([0., 0., 0.])
            pt_max = np.array([800., 600., 1.])
            norm_pt = scale_point(pt, pt_min, pt_max)
            self.audio.set_gain(norm_pt[1])
         else:
            self.kinect.on_update()

            head_pt = self.kinect.get_joint(joint)
            print head_pt
            pt_min = np.array([-1000.0, -1000, 0])
            pt_max = np.array([1000.0, 1000, 2000])

            norm_pt = scale_point(head_pt, pt_min, pt_max)
            self.label.text = '\n'.join([str(x) for x in head_pt])

            self.audio.set_gain(min(1,max(0.01,(norm_pt[1] - 0.3) / .4)))
            self.gainLabel.text = str(self.audio.get_gain())

            # for head
            #self.gainLabel.text = str((1 - norm_pt[2] - 0.4) / .1)#str( (1 - norm_pt[2] - 0.3) / .2)
            #self.audio.set_gain(min(1,max(0.01,(1 - norm_pt[2] - 0.4) / .1)))
         if kUseGlass == False:
            if self.nextNoteCueOnLeft and norm_pt[0] < 0.5: 
               self.songPlayer.playNextNote()
               self.nextNoteCueOnLeft = False
               self.audio.set_gain(norm_pt[1])

            elif self.nextNoteCueOnLeft == False and norm_pt[0] > 0.5:
               self.songPlayer.playNextNote()
               self.nextNoteCueOnLeft = True
               #self.audio.set_gain(norm_pt[2])
               #print norm_pt[]
            self.head.set_pos(norm_pt)
# convert pt into unit scale (ie, range [0,1]) assuming that pt falls in the
# the range [min_val, max_val]
# value is clipped [0,1]
def scale_point(pt, min_val, max_val):
   pt = (pt - np.array(min_val)) / (np.array(max_val) - np.array(min_val))
   pt = np.clip(pt, 0, 1)
   return pt

   # pass in which MainWidget to run as a command-line arg
run(MainWidget)
