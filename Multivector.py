#Notas:
##Entrada do delta tem que ser 2 blades
##Entrada da inversa tem que ser versor

import collections
import Metric
import OrthogonalMetric
from Euclidian import Euclidian

class Multivector:

	def __init__(self):
		self.OP_OUTER_PRODUCT = 1
		self.OP_REGRESSIVE_PRODUCT = 2
		self.OP_GEOMETRIC_PRODUCT = 3
		self.OP_LEFT_CONTRACTION = 4
		self.mv = collections.OrderedDict()

	def __add__(self, other):
		result = Multivector()
		iterSelf = iter(sorted(self.mv.keys()))
		iterOther = iter(sorted(other.mv.keys()))
		mask1 = next(iterSelf, None)
		mask2 = next(iterOther, None)
		while (mask1 is not None) and (mask2 is not None):
			if (mask1 < mask2):
				result.overrideBase(self.mv[mask1], mask1)
				mask1 = next(iterSelf, None)
			elif (mask1 > mask2):
				result.overrideBase(other.mv[mask2], mask2)
				mask2 = next(iterOther, None)
			else:
				result.overrideBase(self.mv[mask1] + other.mv[mask2], mask1)
				mask1 = next(iterSelf, None)
				mask2 = next(iterOther, None)
		while (mask1 is not None):
			result.overrideBase(self.mv[mask1], mask1)
			mask1 = next(iterSelf, None)
		while (mask2 is not None):
			result.overrideBase(other.mv[mask2], mask2)
			mask2 = next(iterOther, None)
		return result

	def __radd__(self, other):
		return other + self

	def __sub__(self, other):
		return self + (-other)

	def __neg__(self):
		for (mask, coef) in self.mv.items():
			self.mv[mask] = -coef
		return self

	def __mul__(self, factor):
		if (isinstance(factor, int)):
			for (mask, coef) in self.mv.items():
				self.mv[mask] = factor * coef
			return self

	def __rmul__(self, factor):
		return self * factor


	def multiOperator(self, other, operation, metric = None):
		result = Multivector()
		if (metric is None):
			metric = Euclidian()
		for mask1, coef1 in self.mv.items():
			for mask2, coef2 in other.mv.items():
				if (operation == self.OP_OUTER_PRODUCT):
					coef, mask = Multivector.OP_COMPONENT(coef1, mask1, coef2, mask2)
				elif (operation == self.OP_REGRESSIVE_PRODUCT):
					coef, mask = Multivector.RP_COMPONENT(coef1, mask1, coef2, mask2) #Dimension missing
				elif (operation == self.OP_GEOMETRIC_PRODUCT):
					coef, mask = Multivector.GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
				elif (operation == self.OP_LEFT_CONTRACTION):
					coef, mask = Multivector.LCONT_COMPONENT(coef1, mask1, coef2, mask2, metric)
				result.insertBase(coef, mask)
		return result

	def __xor__(self, other): #Outer product, ^ is for xor-ing in Python, so...
		return self.multiOperator(other, self.OP_OUTER_PRODUCT)

	def OP(self, other):
		return __xor__(other)

	@staticmethod
	def OP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int):
		if (mask1 & mask2 == 0):
			signal = Multivector.CANON_REORDER(mask1, mask2)
			coefResult = signal * coef1 * coef2
			maskResult = mask1 | mask2
			return (coefResult, maskResult)
		else:
			return (0.0, 0)

	def RP(self, other):
		return self.multiOperator(other, self.OP_REGRESSIVE_PRODUCT)


	@staticmethod
	def RP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, dimension: int): #How to dimension?
		maskResult = mask1 & mask2
		if (GRADE(mask1) + GRADE(mask2) - GRADE(maskResult) == dimension):
			signal = CANON_REORDER(mask1 ^ mask2, mask2 ^ maskResult)
			coefResult = signal * coef1 * coef2
		else:
			coefResult = 0
			maskResult = 0
		return (coefResult, maskResult)

	def GP(self, other, metric: Metric = None):
		return self.multiOperator(other, self.OP_GEOMETRIC_PRODUCT, metric)

	@staticmethod
	def GP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
		signal = Multivector.CANON_REORDER(mask1, mask2)
		metric = metric.factor(mask1 & mask2)
		coefResult = signal * metric * coef1 * coef2
		maskResult = mask1 ^ mask2
		return (coefResult, maskResult)

	def LCONT(self, other, metric: Metric = None):
		return self.multiOperator(other, self.OP_LEFT_CONTRACTION, metric)

	def RCONT(self, other, metric: Metric = None):
		return other.multiOperator(self, self.OP_LEFT_CONTRACTION, metri)

	@staticmethod
	def LCONT_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
		coefResult, maskResult = Multivector.GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
		if (Multivector.GRADE(maskResult) == Multivector.GRADE(mask2) - Multivector.GRADE(mask1)):
			return (coefResult, maskResult)
		else:
			return (0, 0)

	# @staticmethod
	# def TAKE_GRADE(self, grade: int):
	# 	for mask, coef in self.mv.items():
	# 		if (GRADE(mask) == grade):
	# 			return (coef, mask)
	# 	return (0, 0)

	@staticmethod	
	def CANON_REORDER(mask1: int, mask2: int):
		changes = 0
		mask1 //= 2
		while (mask1 != 0):
			changes += Multivector.GRADE(mask1 & mask2)
			mask1 //= 2
		if (changes & 1 == 0):
			return 1
		else:
			return -1

	@staticmethod
	def GRADE(mask: int):
		result = 0
		while (mask > 0):
			if (mask % 2 == 1):
				result += 1
			mask //= 2
		return result

	def overrideBase(self, coef: float, mask: int):
		if (coef != 0):
			self.mv[mask] = coef
		else:
			del self.mv[mask]

	def insertBase(self, coef: float, mask: int):
		if (coef != 0):
			if mask in self.mv:
				self.mv[mask] += coef
			else:
				self.overrideBase(coef, mask)


	def removeBase(self, coef: int):
		overrideBase(coef, 0)

	@staticmethod
	def e_coef(coef: float, base: int):
		if (base < 1):
			return None
		mv = Multivector()
		mv.overrideBase(coef, pow(2, base - 1))
		return mv

	@staticmethod
	def e(base: int):
		return Multivector.e_coef(1.0, base)