from __future__ import division

####################
# GLOVE AUDIO file #
####################

import sys
sys.path.append('../common')
from core import *
from audio import *
from clock import *
from song import *
from wavegen import *
from synth import *

import random
import numpy as np
import bisect
from collections import namedtuple

# reads in audio files.
# note spec:
#   [num_notes_in_line],[duration]:allowed_note_1, [...], allowed_note_5
# mapping of notes to fingers
# example
#   16,16:C4,E4,G4,C5,E5

class GloveAudioData(object):

  note_to_num = {\
      "B#":0,"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,"Fb":4,"E#":5,"F":5,\
      "F#":6,"Gb":6,"G":7,"G#":8,"Ab":8,"A":9,"A#":10,"Bb":10,"B":11,"Cb":11}
  num_to_note = {\
      0:"B#",0:"C",1:"C#",1:"Db",2:"D",3:"D#",3:"Eb",4:"E", 4:"Fb",5:"E#",5:"F",\
      6:"F#",6:"Gb",7:"G",8:"G#",8:"Ab",9:"A",10:"A#",10:"Bb",11:"B",11:"Cb"}

  def __init__(self, filepath):
    super(GloveAudioData, self).__init__()
    self.notes = []
    self._read_note_data(filepath)

  def _read_note_data(self, filepath):
    lines = open(filepath).read().split('\n')
    print "lines in file", len(lines)
    for line in lines:
      if "," in line:
        first_half, second_half = line.split(":")
        # Get the number of notes this applies to, and the duration
        num_notes, duration = first_half.split(",")
        # Get the allowed notes
        note_list = second_half.split(",")
        # translate the notes in our list from letters to MIDI
        midi_notes = self.notes_to_midi(note_list)
        # Append the notes to our notes list
        for n in range(int(num_notes)):
          self.notes.append((int(duration), midi_notes))

  def notes_to_midi(self, note_strs):
    midi_notes = []
    for n in note_strs:
      note_only = n.translate(None,"0123456789")
      oct_only = n.translate(None,"ABCDEFGb#")
      midi_note = self.note_to_num[note_only] + int(oct_only) * 12
      midi_notes.append(midi_note)
    return midi_notes

  def get_note_at(self, idx):
    return self.notes[idx % len(self.notes)]

kSecondsPerQuarter = 0.5

# keeps track of where we are in the song
# plays next note
class GloveAudioPlayer(object):
  def __init__(self, data, settings):
    super(GloveAudioPlayer, self).__init__()
    self.data = data
    self.audio = Audio()
    self.synth = Synth("../common/FluidR3_GM.sf2")
    self.chan, self.bank, self.preset = settings
    self.synth.program(*settings)
    self.audio.add_generator(self.synth)
    self.idx = 0
    self.cur_notes = []
    self.cur_notes_durations = []

  # play the next note, finger is a number 0-4
  def play_next_note(self, finger):
    duration, notes = self.data.get_note_at(self.idx)
    duration = (4/(duration) * 0.5)
    self.synth.noteon(self.chan, notes[finger], 127)
    self.cur_notes.append((duration, notes[finger]))
    self.cur_notes_durations.append(0)
    self.idx += 1

  def on_update(self, dt):
    remove_list = []
    idx = 0
    for n in self.cur_notes:
      self.cur_notes_durations[idx] += dt
      if self.cur_notes_durations[idx] > self.cur_notes[idx][0]:
        self.synth.noteoff(self.chan, self.cur_notes[idx][1])
        self.cur_notes.remove(self.cur_notes[idx])
        self.cur_notes_durations.remove(self.cur_notes_durations[idx])
      else:
        idx += 1

