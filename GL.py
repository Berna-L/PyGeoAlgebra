import GA
import pyglet
from Multivector import Multivector
from Camera import Camera
from pyglet.gl import *

win = pyglet.window.Window(width=1600, height=900)

# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=win.width//2, y=win.height//2,
#                           anchor_x='center', anchor_y='center')

points = []

def multivector_to_point(p):
  grade = GA.GRADE(p)
  points_qty = 0
  result = (0, 0)
  if (grade is 1): #Point
    if (p[0b1000] != 0): #Proper point
      print("aqui")
      points_qty = 1
      result = (p[0b0001], p[0b0010], p[0b0100], p[0b1000])
    else: #Improper point/direction
      points_qty = 0
  elif (grade is 2):
    pass #????????
  elif (grade is 3): #Line
      points_qty = 2 #???????
      # result = (p[])
  return (points_qty, result)


@win.event
def on_draw():
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        for p in points:
          (points_qty, converted) = multivector_to_point(camera.transform(p))
          print("Coordenadas convertidas:", converted)
          if (points_qty > 1):
            glBegin(GL_LINE_LOOP)
          else:
            glBegin(GL_POINTS)  
          for i in range(0, points_qty):
            glVertex4f(converted[i], converted[i + 1], converted[i + 2], converted[i + 3])
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
point[0b0010] = -300
point[0b1000] = 1

points.append(point)
# points.append((Multivector.e(1) * 10 + Multivector.e(3) * 2 + Multivector.e(4)) ^ (Multivector.e(2) * -1 + Multivector.e(3) * 2 + Multivector.e(4)))
# points.append(Multivector.e(1) * -10 + Multivector.e(2) * -10 + Multivector.e(4))
# points.append(Multivector.e(3) * -10)
# points.append(Multivector.e(1) * -100 + Multivector.e(3) * -10 + Multivector.e(4) * 0.1)

# print(o ^ J)

# p1 = Multivector.e(1) + Multivector.e(4)
# p2 = Multivector.e(2) + Multivector.e(4)
# print(p1 ^ p2)

pyglet.app.run()