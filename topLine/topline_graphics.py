import sys
sys.path.append('../common')
from core import *
from graphics import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup



class ToplineGraphics(InstructionGroup):

	def __init__(self, gloveGraphics):
		super(ToplineGraphics, self).__init__()

		self.cursor = Cursor3D((780,180), (10, 400), gloveGraphics.future_color, False)
		self.add(self.cursor)

		self.verticalLine = Line(points=[400,400,400,580])
		self.add(self.verticalLine)
		self.gloveGraphics = gloveGraphics

	def set_pos(self,pos):
		pos[2] = 0.1
		self.cursor.set_pos(pos)

	def note_hit(self):
		self.gloveGraphics.on_topline_note_hit()