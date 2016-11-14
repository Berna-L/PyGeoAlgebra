#Notas:
##Entrada do delta tem que ser 2 blades
##Entrada da inversa tem que ser versor

import collections
import Metric
import OrthogonalMetric
import Euclidian

class Multivector(object):

	def __init__(self):
		self.mv = collections.OrderedDict()

	def __add__(self, other):
		result = Multivector()
		iterSelf = iter(sorted(self.masks()))
		iterOther = iter(sorted(other.masks()))
		mask1 = next(iterSelf, None)
		mask2 = next(iterOther, None)
		while (mask1 is not None) and (mask2 is not None):
			if (mask1 < mask2):
				result.overrideBase(self[mask1], mask1)
				mask1 = next(iterSelf, None)
			elif (mask1 > mask2):
				result.overrideBase(other[mask2], mask2)
				mask2 = next(iterOther, None)
			else:
				result.overrideBase(self[mask1] + other[mask2], mask1)
				mask1 = next(iterSelf, None)
				mask2 = next(iterOther, None)
		while (mask1 is not None):
			result.overrideBase(self[mask1], mask1)
			mask1 = next(iterSelf, None)
		while (mask2 is not None):
			result.overrideBase(other[mask2], mask2)
			mask2 = next(iterOther, None)
		return result

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		return self + (-other)

	def __neg__(self):
		result = Multivector()
		for (mask, coef) in self.items():
			result[mask] = -coef
		return result

	def __mul__(self, other):
		if (isinstance(other, int) or isinstance(other, float)):
			result = Multivector()
			for (mask, coef) in self.items():
				result[mask] = other * coef
			return result
		elif (isinstance(other, Multivector)):
			from GA import Operation
			import GA
			return GA.multiOperator(self, other, GA.Operation.BLADES_SCALAR_PRODUCT)
		else:
			raise TypeError("Must multiply by a scalar or other Multivector")

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		if (isinstance(other, int) or isinstance(other, float)):
			result = Multivector()
			for (mask, coef) in self.items():
				result[mask] = other / coef
			return result
		elif (isinstance(other, Multivector)):
			from GA import Operation
			import GA
			return GA.multiOperator(self, GA.INVERSE(other), GA.Operation.GEOMETRIC_PRODUCT)
		else:
			raise TypeError("Must divide by a scalar or other Multivector")

	def __getitem__(self, key):
		return self.mv[key]

	def __setitem__(self, key, value):
		self.mv[key] = value

	def __eq__(self, other):
		iterSelf = iter(sorted(self.masks()))
		iterOther = iter(sorted(other.masks()))
		mask1 = next(iterSelf, None)
		mask2 = next(iterOther, None)
		while (mask1 is not None) and (mask2 is not None):
			if (mask1 < mask2):
				return False
			elif (mask1 > mask2):
				return False
			else:
				if (self[mask1] != other[mask2]):
					return False
				mask1 = next(iterSelf, None)
				mask2 = next(iterOther, None)
		while (mask1 is not None):
			return False
		while (mask2 is not None):
			return False
		return True

	def items(self):
		return self.mv.items()

	def masks(self):
		return self.mv.keys()

	def coefs(self):
		return self.mv.values()

	# def multiOperator(self, other, operation, metric = None):
	# 	result = Multivector()
	# 	if (metric is None):
	# 		metric = Euclidian()
	# 	for mask1, coef1 in self.mv.items():
	# 		for mask2, coef2 in other.mv.items():
	# 			if (operation == self.OP_OUTER_PRODUCT):
	# 				coef, mask = Multivector.OP_COMPONENT(coef1, mask1, coef2, mask2)
	# 			elif (operation == self.OP_REGRESSIVE_PRODUCT):
	# 				coef, mask = Multivector.RP_COMPONENT(coef1, mask1, coef2, mask2) #Dimension missing
	# 			elif (operation == self.OP_GEOMETRIC_PRODUCT):
	# 				coef, mask = Multivector.GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
	# 			elif (operation == self.OP_LEFT_CONTRACTION):
	# 				coef, mask = Multivector.LCONT_COMPONENT(coef1, mask1, coef2, mask2, metric)
	# 			elif (operation == self.OP_BLADES_SCALAR_PRODUCT):
	# 				coef, mask = Multivector.SCP_COMPONENT(coef1, mask1, coef2, mask2, metric)
	# 			result.insertBase(coef, mask)
	# 	return result

	def __xor__(self, other): #Outer product, ^ is for xor-ing in Python, so...
		from GA import Operation
		import GA
		return GA.multiOperator(self, other, GA.Operation.OUTER_PRODUCT)

	# def REVERSE(mv):
	# 	result = Multivector()
	# 	for coef, mask in mv.items():
	# 		k = Multivector.GRADE(mask)
	# 		result[mask] = coef * pow(-1, (k * (k - 1)) / 2)

	# def SQR_NORM_REV(self):
	# 	return self.SCP(self.REVERSE())

	# def OP(self, other):
	# 	return __xor__(other)

	# @staticmethod
	# def OP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int):
	# 	if (mask1 & mask2 == 0):
	# 		signal = Multivector.CANON_REORDER(mask1, mask2)
	# 		coefResult = signal * coef1 * coef2
	# 		maskResult = mask1 | mask2
	# 		return (coefResult, maskResult)
	# 	else:
	# 		return (0.0, 0)

	# def RP(self, other):
	# 	return GA.multiOperator(self, other, GA.Operation.REGRESSIVE_PRODUCT)


	# @staticmethod
	# def RP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, dimension: int): #How to dimension?
	# 	maskResult = mask1 & mask2
	# 	if (GRADE(mask1) + GRADE(mask2) - GRADE(maskResult) == dimension):
	# 		signal = CANON_REORDER(mask1 ^ mask2, mask2 ^ maskResult)
	# 		coefResult = signal * coef1 * coef2
	# 	else:
	# 		coefResult = 0
	# 		maskResult = 0
	# 	return (coefResult, maskResult)

	# def GP(self, other, metric: Metric = None):
	# 	return GA.multiOperator(self, other, GA.Operation.GEOMETRIC_PRODUCT, metric)

	# @staticmethod
	# def GP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
	# 	signal = Multivector.CANON_REORDER(mask1, mask2)
	# 	metric = metric.factor(mask1 & mask2)
	# 	coefResult = signal * metric * coef1 * coef2
	# 	maskResult = mask1 ^ mask2
	# 	return (coefResult, maskResult)

	# def LCONT(self, other, metric: Metric = None):
	# 	return GA.multiOperator(self, other, GA.Operation.LEFT_CONTRACTION, metric)

	# def RCONT(self, other, metric: Metric = None):
	# 	return GA.multiOperator(other, self, GA.Operation.LEFT_CONTRACTION, metric)

	# @staticmethod
	# def LCONT_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
	# 	coefResult, maskResult = Multivector.GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
	# 	if (Multivector.GRADE(maskResult) == Multivector.GRADE(mask2) - Multivector.GRADE(mask1)):
	# 		return (coefResult, maskResult)
	# 	else:
	# 		return (0, 0)

	# def SCP(self, other, metric: Metric = None):
		# return GA.multiOperator(other, GA.Operation.BLADES_SCALAR_PRODUCT, metric)

	# @staticmethod
	# def SCP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
	# 	if (Multivector.GRADE(mask1) == Multivector.GRADE(mask2)):
	# 		coefResult, maskResult = Multivector.GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
	# 		return (coefResult, maskResult)
	# 	else:
	# 		return (0, 0)


	# @staticmethod
	# def TAKE_GRADE(self, grade: int):
	# 	for mask, coef in self.mv.items():
	# 		if (GRADE(mask) == grade):
	# 			return (coef, mask)
	# 	return (0, 0)

	# @staticmethod	
	# def CANON_REORDER(mask1: int, mask2: int):
	# 	changes = 0
	# 	mask1 //= 2
	# 	while (mask1 != 0):
	# 		changes += Multivector.GRADE(mask1 & mask2)
	# 		mask1 //= 2
	# 	if (changes & 1 == 0):
	# 		return 1
	# 	else:
	# 		return -1

	# @staticmethod
	# def GRADE(mask: int):
	# 	result = 0
	# 	while (mask > 0):
	# 		if (mask % 2 == 1):
	# 			result += 1
	# 		mask //= 2
	# 	return result

	def overrideBase(self, coef: float, mask: int):
		if (mask != 0 or coef != 0):
			self[mask] = coef
		else:
			self.removeBase(mask)

	def insertBase(self, coef: float, mask: int):
		if mask in self.mv:
			self[mask] += coef
		else:
			self.overrideBase(coef, mask)


	def removeBase(self, mask: int):
		try:
			del self.mv[mask]
		except KeyError:
			pass

	@staticmethod
	def e_coef(coef: float, base: int):
		if (base < 1):
			return None
		mv = Multivector()
		mv.overrideBase(coef, pow(2, base - 1))
		return mv

	eSingleton = [None] * 50

	@staticmethod
	def e(base: int):
		if (Multivector.eSingleton[base] is None):
			Multivector.eSingleton[base] = Multivector.e_coef(1.0, base)
		return Multivector.eSingleton[base]