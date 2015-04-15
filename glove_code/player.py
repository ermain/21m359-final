from __future__ import division
# things which play other things when triggered
# common import

import sys
sys.path.append('./common')
from core import *
from audio import *
from synth import *
from wavegen import *

# This class is a simple note player that knows how to play a note on and will
# automatically call the note off some time later. Remember to call on_update()
# on it.
class NotePlayer(object):
  def __init__(self, synth, chan_settings):
    super(NotePlayer, self).__init__()
    self.synth = synth
    for c in chan_settings:
      self.synth.program(*c)
    self.notes = []

  def play_note(self, pitch, velocity, duration, idx):
    self.synth.noteon(idx, pitch, velocity)
    self.notes.append([duration, idx, pitch])

  def on_update(self, dt):
    for n in self.notes:
      n[0] -= dt
      if n[0] <= 0:
        self.synth.noteoff(n[1], n[2])
        self.notes.remove(n)

# like the note player, this is a collection of snippets that can be played.
class SnippetPlayer(object):
  #reader = WaveReader("hbfs.wav")
  #regions = SongRegions("hbfs_regions.txt")
  #snippets = make_snippets(regions, reader)
  def __init__(self, audio):
    self.audio = audio

  def play_snippet(self, word):
   # gen = self.snippets[word].make_generator(0,1)
    self.audio.add_generator(gen)
