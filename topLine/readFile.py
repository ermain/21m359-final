NOTE_TO_MIDI = {'C4':48,
'G3':43,
'C#4':49,
'D4':50,
'D#4':51,
'E4':52,
'F4':53,
'F#4':54,
'G4':55,
'G#4':56,
'A4':57,
'A#4':58,
'B4':59,
'C5':60,
'C#5':61,
'D5':62,
'D#5':63,
'E5':64,
'F5':65,
'F#5':66,
'G5':67,
'G#5':68,
'A5':69,
'A#5':70,
'B5':71,
'C6':72,
'D6':74,
'E6':76}
import re
def noteToMidi(noteString):
	return NOTE_TO_MIDI[noteString]

class SongData():
	def __init__(self):
		self.songElements = []

	def addElement(self, songElement):
		self.songElements.append(songElement)


class SongElement():
	def __init__(self, note, duration, dynamics):
		self.note = note
		self.duration = duration
		self.dynamics = dynamics
		if note != 'R':
			self.midiNumber = noteToMidi(note)
		else:
			self.midiNumber = None
	def __str__(self):
		return self.note + " " + self.duration + " " + self.dynamics

def parseSong():
	f = open('./topLine/solo.txt', 'r')
	sd = SongData()
	for line in f:
		line = line.split("//")[0]
		if line != '':
	   		info =  re.split(r'\t+', line)
	   		if len(info)== 3:
	   			note, duration, dynamics = info
	   			note = note.strip()
	   		else:
	   			note, duration = info
	   			dynamics = ''
	   		se = SongElement(note, duration, dynamics)
	   		sd.addElement(se)
	return sd







