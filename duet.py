# common import
import sys
sys.path.append('./common')
from core import *
from graphics import *
from synth import *
from audio import *

sys.path.append('./glove')
from glove_audio import *
from glove_graphics import *
from glove_input import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock
from kivy.core.image import Image

sys.path.append('./topLine')
from topline_audio import *
from topline_graphics import *
from topline_input import *

import random
import numpy as np

from kinect import *

kUseKinect = True 
kUsingGlove = False

class MainWidget(BaseWidget) :
   def __init__(self):
      super(MainWidget, self).__init__()
  
      self.audio = Audio()
      self.synth = Synth('common/FluidR3_GM.sf2')
      self.synth.program(0, 0, 40) #violin
      self.audio.add_generator(self.synth)
   
      # for bottom line / glove
      self.glove_audio_data = GloveAudioData("./glove/prelude_notes.txt")
      self.glove_audio_player = GloveAudioPlayer(self.glove_audio_data, (1,0,0), \
         self.synth, self.audio)  
    
      self.note_data = GloveDisplayData("./glove/prelude_visuals.txt")
      glove_pos = (400, 50)
      self.note_display = GloveNoteDisplay(glove_pos, "./glove/circletexture.png", self.note_data)
      self.canvas.add(self.note_display)
      self.scroller = Scroller(self.note_display)

      self.glove_input = GloveInput(self.glove_audio_player.play_next_note, \
          self.note_display.on_note_hit, self.scroller.on_glove_hit, kUsingGlove)

      self.glove_info = GloveInfo(self.glove_input, self.glove_audio_player.audio)
      #self.add_widget(self.glove_info)
      
      # for top line
      self.songPlayer = SongPlayer(self.synth,0)

      self.nextNoteCueOnLeft =  True
      self.start = False

      self.topline_graphics = ToplineGraphics(self.note_display)
      self.canvas.add(self.topline_graphics)

      if kUseKinect:
         self.topline_input = KinectTopLine(self.songPlayer, self.topline_graphics)
      else:
         self.topline_input = ScreenTopLine(self.songPlayer, self.topline_graphics)

   def on_touch_down(self,touch):
      
      print touch.pos

   def on_key_down(self, keycode, modifiers):

      if keycode[1] == 'c':
         self.topline_input.calibrateHeadHeight()

      if keycode[1] == 's':
         if self.topline_input.settingsMode == False:
            self.start = True
            self.topline_input.toSettingsMode()
            self.songPlayer.pause()
            self.topline_graphics.settingsMode()
         
      if keycode[1] == 'p':
         self.start = True
         self.topline_input.toPlayMode()
         self.topline_graphics.duetMode()

      if self.start == True:
         self.glove_input.on_button_down(keycode)
   
   def on_key_up(self, keycode):
      if self.start == True:
         self.glove_input.on_button_up(keycode)

   def on_update(self) :
      
      dt = kivyClock.frametime
      if self.start:

         # start glovestuff
         self.glove_audio_player.on_update(dt)
         self.glove_input.on_update()
         self.glove_info.on_update()
         self.note_display.on_update(dt)
         # end glovestuff
         
         pt = [Window.mouse_pos[0], Window.mouse_pos[1], 0]
         self.topline_input.on_update(pt)

         if not self.topline_input.settingsMode:
            self.songPlayer.on_update(dt)
            self.topline_graphics.meshOn = self.songPlayer.notePlaying
            self.topline_graphics.on_update(dt, self.songPlayer.notePlayer.currentGain)

def scaledX(x, min_val, max_val, a, b):
   return a + ((b-a)*(x-min_val)) / (max_val - min_val)

run(MainWidget)
