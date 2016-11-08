from Multivector import Multivector
import Metric
import OrthogonalMetric
from Euclidian import Euclidian

from enum import Enum

class Operation(Enum):
	OUTER_PRODUCT = 2
	REGRESSIVE_PRODUCT = 3
	GEOMETRIC_PRODUCT = 4
	BLADES_SCALAR_PRODUCT = 5
	LEFT_CONTRACTION = 6


def multiOperator(mv1, mv2, operation, metric = None, dimensions = -1):
	result = Multivector()
	if (metric is None):
		metric = Euclidian()
	for mask1, coef1 in mv1.items():
		for mask2, coef2 in mv2.items():
			if (operation is Operation.OUTER_PRODUCT):
				coef, mask = OP_COMPONENT(coef1, mask1, coef2, mask2)
			elif (operation is Operation.REGRESSIVE_PRODUCT):
				if (dimensions >= 0):
					coef, mask = RP_COMPONENT(coef1, mask1, coef2, mask2, dimensions)
				else:
					raise ValueError("Dimensão precisa ser informaada")
			elif (operation is Operation.GEOMETRIC_PRODUCT):
				coef, mask = GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
			elif (operation is Operation.LEFT_CONTRACTION):
				coef, mask = LCONT_COMPONENT(coef1, mask1, coef2, mask2, metric)
			elif (operation is Operation.BLADES_SCALAR_PRODUCT):
				coef, mask = SCP_COMPONENT(coef1, mask1, coef2, mask2, metric)
			result.insertBase(coef, mask)
	return result



def MUL(mv, other):
	if (isinstance(other, int) or isinstance(other, float)):
		result = Multivector()
		for (mask, coef) in self.items():
			result[mask] = other * coef
		return result
	elif (isinstance(other, Multivector)):
			return multiOperator(other, Operation.BLADES_SCALAR_PRODUCT)
	else:
		raise TypeError("Multiplicação com ftorres inválidos")



def REVERSE(mv):
	result = Multivector()
	for coef, mask in mv.items():
		k = GRADE(mask)
		result[mask] = coef * pow(-1, (k * (k - 1)) / 2)

def SQR_NORM_REV(mv):
	return SCP(REVERSE(mv))

def OP(mv1, mv2):
	return multiOperator(mv1, mv2, Operation.OUTER_PRODUCT)


def OP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int):
	if (mask1 & mask2 == 0):
		signal = CANON_REORDER(mask1, mask2)
		coefResult = signal * coef1 * coef2
		maskResult = mask1 | mask2
		return (coefResult, maskResult)
	else:
		return (0.0, 0)

def RP(mv1, mv2):
	return multiOperator(mv1, mv2, Operation.REGRESSIVE_PRODUCT)


def RP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, dimension: int): #How to dimension?
	maskResult = mask1 & mask2
	if (GRADE(mask1) + GRADE(mask2) - GRADE(maskResult) == dimension):
		signal = CANON_REORDER(mask1 ^ mask2, mask2 ^ maskResult)
		coefResult = signal * coef1 * coef2
	else:
		coefResult = 0
		maskResult = 0
	return (coefResult, maskResult)

def GP(mv1, mv2, metric: Metric = None):
	return multiOperator(mv1, mv2, Operation.GEOMETRIC_PRODUCT, metric)


def GP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
	signal = CANON_REORDER(mask1, mask2)
	metric = metric.factor(mask1 & mask2)
	coefResult = signal * metric * coef1 * coef2
	maskResult = mask1 ^ mask2
	return (coefResult, maskResult)

def LCONT(mv1, mv2, metric: Metric = None):
	return multiOperator(mv1, mv2, Operation.LEFT_CONTRACTION, metric)

def RCONT(mv1, mv2, metric: Metric = None):
	return multiOperator(mv2, mv1, Operation.LEFT_CONTRACTION, metric)


def LCONT_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
	coefResult, maskResult = GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
	if (GRADE(maskResult) == GRADE(mask2) - GRADE(mask1)):
		return (coefResult, maskResult)
	else:
		return (0, 0)

def SCP(mv1, mv2, metric: Metric = None):
	return multiOperator(mv1, mv2, Operation.BLADES_SCALAR_PRODUCT, metric)


def SCP_COMPONENT(coef1: float, mask1: int, coef2: float, mask2: int, metric: OrthogonalMetric):
	if (GRADE(mask1) == GRADE(mask2)):
		coefResult, maskResult = GP_COMPONENT(coef1, mask1, coef2, mask2, metric)
		return (coefResult, maskResult)
	else:
		return (0, 0)

#Métodos auxiliares

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

def GRADE(mask: int):
	result = 0
	while (mask > 0):
		if (mask % 2 == 1):
			result += 1
		mask //= 2
	return result

def TAKE_GRADE(mv, grade: int):
	for mask, coef in mv.items():
		if (GRADE(mask) == grade):
			return (coef, mask)
	return (0, 0)

