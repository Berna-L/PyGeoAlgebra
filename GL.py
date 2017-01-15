import pyglet
from Multivector import Multivector
from Camera import Camera
from pyglet.gl import *

win = pyglet.window.Window(width=640, height=480)

# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=win.width//2, y=win.height//2,
#                           anchor_x='center', anchor_y='center')

points = []

def multivector_to_3d_point(p):
  point = (p[0b001], p[0b010])
  return point

@win.event
def on_draw():
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT)


        glBegin(GL_TRIANGLES)
        for p in points:
          converted = multivector_to_3d_point(p)
          glVertex2f(converted[0], converted[1])

        glEnd()

o = Multivector()
o[0b001] = 1
o[0b010] = 1
o[0b100] = 1

J = Multivector()
J[0b0011] = 0.5
# J[0b1000] = 1

z = Multivector.e(3)

camera = Camera(o, J, z)

point = Multivector.e(3) * 800
point[0b001] = 300

points.append(camera.transform_point(point))
points.append(camera.transform_point(Multivector.e(3) * 200))
points.append(camera.transform_point(Multivector.e(3) * 400))


# print(points[0])

pyglet.app.run()