import sys
sys.path.append('../common')
from core import *
from graphics import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Mesh, Rectangle
from kivy.core.image import Image
from kivy.core.window import Window


class ToplineGraphics(InstructionGroup):

	def __init__(self, gloveGraphics):
		super(ToplineGraphics, self).__init__()

		self.segments = 800

		self.meshOn = True
		#self.drawMesh()
		self.timeSinceUpdate = 0
		self.add(Color((149/255, 165/255, 166/255)))

		self.verticalLine = Line(points=[Window.size[0]/2.,0,Window.size[0]/2,Window.size[1]])
		self.add(self.verticalLine)
		

		self.gloveGraphics = gloveGraphics
		self.cursor = None
		self.drawGameCursor()
		self.color = Color(1,1,1)
		self.add(self.color)

		self.bodyImage = None
		self.kinectJoint = None

		self.cursorY = None

		#self.add(Color(1,1,1))
		#r = Rectangle(pos=(0,450), size = (Window.size[0],50))
		#self.add( r )

	def redrawVerticalLine(self):
		self.verticalLine.points = [Window.size[0]/2.,0,Window.size[0]/2,Window.size[1]]

	def updateKinectSelection(self, pos):
		if self.kinectJoint:
			self.remove(self.kinectJoint)
		self.kinectJoint = Ellipse(segments = 40, size=(30,30), pos=(pos[0]-15,pos[1]-15) )
		self.add(self.kinectJoint)

	def settingsMode(self):
		self.remove(self.cursor)

		self.drawBodySelectionCursor()
		#self.updateKinectSelection((491,295))

	def drawBodySelectionCursor(self):
		self.bodyImage = Rectangle(source='body.jpg', pos=(Window.size[0]/2. - 150,50), size=(300,600))
		self.add(self.bodyImage)
		self.cursor = Cursor3D((Window.size[0],Window.size[1]), (0, 0), (1,0,0), False)
		self.add(self.cursor)

	def duetMode(self):
		self.remove(self.cursor)
		if self.kinectJoint:
			self.remove(self.kinectJoint)
		if self.bodyImage:
			self.remove(self.bodyImage)
			self.bodyImage = None
		self.drawGameCursor()

	def drawGameCursor(self):
		# 780, MESH_HEIGHT*2 # (10, MESH_Y-MESH_HEIGHT)
		if self.cursor:
			self.remove(self.cursor)
		self.cursor = Cursor3D((Window.size[0],400), (0, 300), self.gloveGraphics.future_color, False)
		self.add(self.cursor)

	def set_pos(self,pos):
		pos[2] = 0.1
		self.cursor.set_pos(pos)
		self.cursorY = pos[1]

	def note_hit(self):
		
		indexOfNote = self.gloveGraphics.on_topline_note_hit()

		return indexOfNote


def scaledX(x, min_val, max_val, a, b):
   return a + ((b-a)*(x-min_val)) / (max_val - min_val)

# a ribbon mesh has a matrix of verticies layed out as 2 x N+1 (rows x columns)
# where N is the # of segments.
def make_ribbon_mesh(x, y, w, h, tex_file, segments):
   mesh = Mesh()

   # create indicies
   mesh.indices = range(segments * 2 + 2)

   # create verticies with evenly spaced texture coordinates
   span = np.linspace(0.0, 1.0, segments + 1)
   verts = []
   for s in span:
      verts += [x + s * w, y, s, 0,  x + s * w, y+h, s, 1]
   mesh.vertices = verts

   # assign texture
   if tex_file:
      mesh.texture = Image(tex_file).texture

   # standard triangle strip mode
   mesh.mode = 'triangle_strip'

   return mesh