import GA
from Multivector import Multivector
import copy
# import Homogeneous

class Camera(object):

	# def __init__(self, o, o_linha, u, v, dimensions):
		# J_blade = copy.deepcopy(J)
		# J_blade[pow(2, dimensions)] = 0 #Version for blade check
		# print(J)
		# print(J_blade)
		# if (GA.IS_BLADE(J_blade) is not True):
			# raise ValueError("J, without the homogeneous coordinate (if set), must be a blade")
		# if (GA.GRADE(z) is not 1):
			# raise ValueError("z must be a 1-dimensional blade")
		# self.o = o
		# self.J = J
		# self.z = z
		# print(z ^ o)
		# mj = GA.MEET_JOIN(o ^ z, J, 4)
		# print(mj)
		# print(GA.RP(J, z ^ o, 4))
		# print(GA.RP(o ^ z, J, 4))

	def __init__(self, o, oInPlane, u, v, dimensions):
		if (GA.GRADE(o) > 1):
			raise ValueError("o must be a proper or improper point")
		if (GA.GRADE(oInPlane) is not 1):
			raise ValueError("oInPlane must be a proper point")
		if (GA.GRADE(u) is not 1 or u[pow(2, dimensions)] != 0):
			raise ValueError("u must be an improper point")
		if (GA.GRADE(v) is not 1 or v[pow(2, dimensions)] != 0):
			raise ValueError("v must be an improper point")
		self.o = o
		self.J = oInPlane ^ u ^ v
		self.z = GA.LCONT(Multivector.e(4), o ^ oInPlane)

	def transform(self, p):
		if (GA.IS_BLADE(p) is not True):
			raise ValueError("p must be a blade")
		print("Ponto atual:", p)
		print("cálculo do PE ", self.o ^ p)
		return GA.RP(self.J, self.o ^ p, 4)