import GA
import Multivector
# import Homogeneous

class Camera(object):

	def __init__(self, o, J, z):
		if (GA.GRADE(o) > 1):
			raise ValueError("o must be a 0 or 1-dimensional blade")
		if (GA.IS_BLADE(J) is not True):
			raise ValueError("J must be a blade")
		if (GA.GRADE(o) is not 1):
			raise ValueError("z must be a 1-dimensional blade")
		self.o = o
		self.J = J
		self.z = z


	# def __init__(self, o, oInPlane, u, v):
	# 	if (GA.GRADE(o) > 2):
	# 		raise ValueError("o must be a 0 or 1-dimensional blade")
	# 	if (GA.GRADE(oInPlane) is not 1):
	# 		raise ValueError("oInPlane must be a 0 or 1-dimensional blade")
	# 	if (GA.GRADE(u) is not 2):
	# 		raise ValueError("u must be a 1-dimensional blade")
	# 	if (GA.GRADE(v) is not 2):
	# 		raise ValueError("v must be a 1-dimensional blade")
	# 	self.o = o
	# 	self.J = oInPlane ^ u ^ v
	# 	self.z = o ^ oInPlane

	def transform_point(self, p):
		if (GA.IS_BLADE(p) is not True):
			raise ValueError("p must be a blade")
		# print("cálculo do PE ", self.o ^ p)
		return GA.RP(self.J, self.o ^ p, 3)