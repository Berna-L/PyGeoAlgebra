from Multivector import Multivector

class GA:
	
	from enum import Enum

	class Operation(Enum):
		SUM = 1
		OUTER_PRODUCT = 2
		REGRESSIVE_PRODUCT = 3
		GEOMETRIC_PRODUCT = 4
		BLADES_SCALAR_PRODUCT = 5
		LEFT_CONTRACTION = 6


	@staticmethod
	def multiOperator(mv1, mv2, operation, metric = None, dimensions = -1):
		result = Multivector()
		if (metric is None):
			metric = Euclidian()
		if (operation is SUM):
			return SUM(mv1, mv2)
		for mask1, coef1 in mv1.items():
			for mask2, coef2 in mv2.items():
				if (operation is OUTER_PRODUCT):
					coef, mask = OP_COMPONENT(coef1, mask1, coef2, mask2)
				elif (operation is REGRESSIVE_PRODUCT):
					if (dimensions >= 0):
						coef, mask = Multivector.RP_COMPONENT(coef1, mask1, coef2, mask2, dimensions)
					else:
						raise ValueError("Dimensão precisa ser informaada")
				elif (operation is GEOMETRIC_PRODUCT):
					coef, mask = Multivector.GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
				elif (operation is LEFT_CONTRACTION):
					coef, mask = Multivector.LCONT_COMPONENT(coef1, mask1, coef2, mask2, metric)
				elif (operation is BLADES_SCALAR_PRODUCT):
					coef, mask = Multivector.SCP_COMPONENT(coef1, mask1, coef2, mask2, metric)
				result.insertBase(coef, mask)
		return result


	@staticmethod
	def SUM(mv1, mv2):
		result = Multivector()
		iterSelf = iter(sorted(mv1.masks()))
		iterOther = iter(sorted(mv2.masks()))
		mask1 = next(iterSelf, None)
		mask2 = next(iterOther, None)
		while (mask1 is not None) and (mask2 is not None):
			if (mask1 < mask2):
				result.overrideBase(mv1[mask1], mask1)
				mask1 = next(iterSelf, None)
			elif (mask1 > mask2):
				result.overrideBase(mv2[mask2], mask2)
				mask2 = next(iterOther, None)
			else:
				result.overrideBase(mv1[mask1] + mv2[mask2], mask1)
				mask1 = next(iterSelf, None)
				mask2 = next(iterOther, None)
		while (mask1 is not None):
			result.overrideBase(mv1[mask1], mask1)
			mask1 = next(iterSelf, None)
		while (mask2 is not None):
			result.overrideBase(mv2[mask2], mask2)
			mask2 = next(iterOther, None)
		return result

	@staticmethod
	def REVERSE(mv):
		result = Multivector()
		for coef, mask in mv.items():
			k = GRADE(mask)
			result[mask] = coef * pow(-1, (k * (k - 1)) / 2)

	@staticmethod
	def OP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int):
		if (mask1 & mask2 == 0):
			signal = Multivector.CANON_REORDER(mask1, mask2)
			coefResult = signal * coef1 * coef2
			maskResult = mask1 | mask2
			return (coefResult, maskResult)
		else:
			return (0.0, 0)

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

	@staticmethod
	def GP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
		signal = CANON_REORDER(mask1, mask2)
		metric = metric.factor(mask1 & mask2)
		coefResult = signal * metric * coef1 * coef2
		maskResult = mask1 ^ mask2
		return (coefResult, maskResult)

	@staticmethod
	def LCONT_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
		coefResult, maskResult = GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
		if (GRADE(maskResult) == GRADE(mask2) - GRADE(mask1)):
			return (coefResult, maskResult)
		else:
			return (0, 0)

	@staticmethod
	def SCP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
		if (GRADE(mask1) == GRADE(mask2)):
			coefResult, maskResult = GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
			return (coefResult, maskResult)
		else:
			return (0, 0)

#Métodos auxiliares

	@staticmethod	
	def CANON_REORDER(mask1: int, mask2: int):
		changes = 0
		mask1 //= 2
		while (mask1 != 0):
			changes += GRADE(mask1 & mask2)
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

	@staticmethod
	def TAKE_GRADE(mv, grade: int):
		for mask, coef in mv.items():
			if (GRADE(mask) == grade):
				return (coef, mask)
		return (0, 0)

