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
					raise ValueError("Dimension must be set")
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
		raise TypeError("Multiplication w/ invalid factors")

def REVERSE(mv):
	result = Multivector()
	for coef, mask in mv.items():
		k = GRADE(mask)
		result[mask] = coef * pow(-1, (k * (k - 1)) / 2)

def INVERSE(mv):
	return REVERSE(mv) / SQR_NORM_REV(mv)

def SQR_NORM_REV(mv):
	return SCP(REVERSE(mv))

def DUAL(mv, dimensions):
	if (dimensions is not None):
		#Pseudo-scalar construction
		maskPseudo = 0
		for i in range(0, dimensions)
			maskPseudo = maskPseudo + pow(2, i)
		pseudo = Multivector()
		pseudo[maskPseudo] = 1
		return LCONT(mv, INVERSE(pseudo))


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

def DELTA_PRODUCT(blade1, blade2):
	if (IS_BLADE(blade1) and IS_BLADE(blade2)):
		mult = GP(blade1, blade2)
		bladeResult = TAKE_GRADE(mult, MAX_GRADE(mult))
		return bladeResult
	raise TypeError("Not a blade")


def MEET_JOIN(blade1, blade2):
	if (IS_BLADE(blade1) and IS_BLADE(blade2)):
		r = GRADE(blade1)
		s = GRADE(blade2)
		if (r > s):
			blade1, blade2 = blade2, blade1
		delta = DELTA_PRODUCT(blade1, blade2)
		t = ((r + s - GRADE(delta)) / 2)
		scalar, factors = BLADE_FACTOR(DUAL(delta))
		meet = 1
		join = Multivector()
		for factor in factors:
			proj = ORTHOGONAL_PROJECTION(factor, blade1)
			if (proj != 0):
				meet = meet ^ proj
				if (GRADE(meet) == t):
					join = RCONT(blade1, INVERSE(meet)) ^ blade2
					break
			rejec = ORTHOGONAL_REJECTION(factor, blade1)
			if (reject != 0):
				join = LCONT(reje, join)
				if (GRADE(join) == r + s - t):
					meet = INVERSE_DUAL(DUAL(B) ^ DUAL(A))
					break
		if (r > s):
			factor = pow(-1, (r-t)*(s-t))
			meet = meet * factor
			join = join * factor
		return meet, join



#Métodos auxiliares

def IS_BLADE(mv):
	try:
		GRADE(mv)
	except ValueError:
		return False
	return True

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

def GRADE(blade: Multivector)
	bladeGrade = None
	for mask in mv.masks():
		currGrade = GRADE(mask)
		if (bladeGrade is None):
			bladeGrade = currGrade
		elif (currGrade != bladeGrade):
			raise ValueError("Must be a blade")
	return currGrade


def MAX_GRADE(mv):
	maxGrade = -1
	for mask in mv.masks():
		currGrade = GRADE(mask)
		if (currGrade > maxGrade):
			maxGrade = currGrade
	return maxGrade

def TAKE_GRADE(mv, grade: int):
	result = Multivector()
	for mask, coef in mv.items():
		if (GRADE(mask) == grade):
			result[mask] = coef
	return result

def MASK_WITH_MAX_ABS_COEF(mv)
	maskResult = -1
	maxCoef = 0
	for mask, coef in mv.items():
		if (abs(coef) > maxCoef):
			maxCoef = abs(coef)
			maskResult = mask
	return maskResult

def BLADE_FACTOR(blade):
	if (IS_BLADE(blade)):
		mask = MASK_WITH_MAX_ABS_COEF(blade)
		scalar = sqrt(SQR_NORM_REV(mv)[0])
		temp = NORMALIZE_BLADE(blade)
		factors = []
		base_vector = 0
		while (mask / 2 != 0):
			base_vector = base_vector + 1
			if (mask % 2 is 1):
				proj = ORTHOGONAL_PROJECTION(Multivector.e(base_vector), temp)
				factors[base_vector] = NORMALIZE_BLADE(proj)
				temp = LCONT(INVERSE(factors[base_vector]), temp)
		base_vector = base_vector + 1
		factors[base_vector] = NORMALIZE_BLADE(temp)
		return scalar, factors

def NORMALIZE_BLADE(blade):
	if (IS_BLADE(blade)):
		return blade / sqrt(SQR_NORM_REV(blade))

def ORTHOGONAL_PROJECTION(mv1, mv2):
	c = LCONT(mv1, mv2)
	result = LCONT(c, INVERSE(mv2))
	return result

def ORTHOGONAL_REJECTION(mv1, mv2):
	c = mv1 ^ mv2
	result = RCONT(c, INVERSE(mv2))
	return result