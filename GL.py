import pyglet
from Multivector import Multivector
from Camera import Camera
from pyglet.gl import *

win = pyglet.window.Window(width=800, height=600)

# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=win.width//2, y=win.height//2,
#                           anchor_x='center', anchor_y='center')

points = []

def multivector_to_point(p):
	point = (p[0b0001], p[0b0010], p[0b0100], p[0b1000])
	return point

@win.event
def on_draw():
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


        glBegin(GL_POINTS)
        for p in points:
          converted = multivector_to_point(camera.transform(p))
          print("Coordenadas convertidas:", converted)
          glVertex4f(converted[0], converted[1], converted[2], converted[3])

        glEnd()

o = Multivector()
o[0b0001] = 0
o[0b0010] = 0
o[0b0100] = 0
o[0b1000] = 1

oInPlane = Multivector()
oInPlane[0b0001] = 0
oInPlane[0b0010] = 0
oInPlane[0b0100] = 1
oInPlane[0b1000] = 1

u = Multivector.e(1)

v = Multivector.e(2)

camera = Camera(o, oInPlane, u, v, 3)

point = Multivector.e(3) * -800
point[0b001] = -300

points.append(point)
points.append(Multivector.e(1) * -10 ^ Multivector.e(2) * 10)
points.append(Multivector.e(1) * -10 + Multivector.e(2) * -10 + Multivector.e(4))
points.append(Multivector.e(3) * -10)
points.append(Multivector.e(1) * -100 + Multivector.e(3) * -10 + Multivector.e(4) * 0.1)

# print(o ^ J)

pyglet.app.run()
