import GA
from Multivector import Multivector

class Camera(object):

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
		print("Regressivo:", GA.RP(self.J, self.o ^ p, 4))
		# (meet, join) = GA.MEET_JOIN(self.J, self.o ^ p, 4)
		# print("meet:", meet)
		return GA.RP(self.J, self.o ^ p, 4)