from readFile import *


class SongPlayer(object):
   def __init__(self, synth, channel):
      super(SongPlayer, self).__init__()

      self.song = parseSong().songElements
      self.indexInSong = 0
      self.notePlayer = NotePlayer(synth, channel)
      self.notePlaying = False

   def playNoteAtIndex(self, index):
      self.indexInSong = index
      songElement = self.song[index]
      pitch = songElement.midiNumber
      duration = songElement.duration
      dynamics = songElement.dynamics
      if pitch != None:
         self.notePlayer.play_note(pitch, 100, duration)
         self.notePlaying = True
      else:
         self.notePlayer.stop_note()
         self.notePlaying = False
      #self.indexInSong += 1

   def updateGain(self, gain):
      self.notePlayer.updateGain(gain)

   def on_update(self,dt):
      self.notePlayer.on_update(dt)

   def pause(self):
      self.notePlayer.stop_note()
      self.notePlaying = False

class NotePlayer(object):
   def __init__(self, synth, channel):
      super(NotePlayer, self).__init__()
      self.synth = synth
      self.timeElapsed = 0
      self.previousPitch = None
      self.channel = channel

      self.desiredGain = 0.5
      self.currentGain = 0.5

   def stop_note(self):
      if self.previousPitch:
         self.synth.noteoff(self.channel, self.previousPitch)

   def play_note(self, pitch, velocity, duration):
      if self.previousPitch:
         self.synth.noteoff(self.channel, self.previousPitch)
      self.synth.noteon(self.channel, pitch, velocity) 
      self.previousPitch = pitch
  
   def updateGain(self, gain):
      self.desiredGain = gain

   def on_update(self,dt):
      if abs(self.desiredGain - self.currentGain) > 0.01:
         gainAdjust = 0.6 * (self.desiredGain - self.currentGain)
         gain = float(gainAdjust + self.currentGain) * 127
         self.currentGain = gainAdjust + self.currentGain
         self.synth.cc(self.channel, 7, int(gain))
