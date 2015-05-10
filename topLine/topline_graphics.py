import sys
sys.path.append('../common')
from core import *
from graphics import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Mesh, Rectangle
from kivy.core.image import Image

MESH_Y = 450.
MESH_HEIGHT = 140
class ToplineGraphics(InstructionGroup):

	def __init__(self, gloveGraphics):
		super(ToplineGraphics, self).__init__()

		self.segments = 800

		self.meshOn = True
		self.drawMesh()
		self.timeSinceUpdate = 0
		self.add(Color((149/255, 165/255, 166/255)))

		self.verticalLine = Line(points=[Window.size[0]/2.,0,Window.size[0]/2,Window.size[1]])
		self.add(self.verticalLine)
		

		self.gloveGraphics = gloveGraphics
		self.drawGameCursor()
		self.color = Color(1,1,1)
		self.add(self.color)

		self.bodyImage = None
		self.kinectJoint = None

		self.cursorY = None

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
		self.bodyImage = Rectangle(source='body.jpg', pos=(250,50), size=(275,500))
		self.add(self.bodyImage)
		self.cursor = Cursor3D((800,600), (0, 0), (1,0,0), False)
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
		self.cursor = Cursor3D((780,MESH_HEIGHT*2), (10, MESH_Y-MESH_HEIGHT), self.gloveGraphics.future_color, False)
		self.add(self.cursor)

	def set_pos(self,pos):
		pos[2] = 0.1
		self.cursor.set_pos(pos)
		self.cursorY = pos[1]

	def note_hit(self):
		return self.gloveGraphics.on_topline_note_hit()

	def drawMesh(self):
		imageFile = './topLine/background.png'
		self.mesh = make_ribbon_mesh(100, MESH_Y, 300-1, MESH_Y, imageFile, self.segments)
		self.add(self.mesh)
		numPoints = len(self.mesh.vertices[5::8])
		self.mesh.vertices[5::8] = [MESH_Y for x in range(0,numPoints)]
		self.mesh.vertices = self.mesh.vertices

		self.meshBottom = make_ribbon_mesh(100, MESH_Y, 300-1, MESH_Y, imageFile, self.segments)
		self.add(self.meshBottom)
		self.meshBottom.vertices[5::8] = [MESH_Y for x in range(0,numPoints)]
		self.meshBottom.vertices = self.mesh.vertices

   	def on_update(self, dt,y):
		self.timeSinceUpdate+=dt

		if self.timeSinceUpdate > 0.01:
			self.timeSinceUpdate = 0

			verticalVerticies = self.mesh.vertices[5::8]
			shiftedDown = verticalVerticies[1:]
			y = scaledX(y,0,1,MESH_Y, MESH_Y+MESH_HEIGHT)
			shiftedDown.append(float(y))
			if not self.meshOn:
				shiftedDown = verticalVerticies[1:]
				shiftedDown.append(MESH_Y)
				self.mesh.vertices[5::8] = [x for x in shiftedDown]
				self.meshBottom.vertices[5::8] = [MESH_Y-(x-MESH_Y) for x in shiftedDown]
			else:
				self.mesh.vertices[5::8] = shiftedDown

				self.meshBottom.vertices[5::8] = [MESH_Y-(x-MESH_Y) for x in shiftedDown]

			self.mesh.vertices = self.mesh.vertices
			self.meshBottom.vertices = self.meshBottom.vertices

		#self.time += kivyClock.frametime

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