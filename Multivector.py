import collections

class Multivector:

	def __init__(self):
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


	def __xor__(self, other): #Outer product, ^ is for xor-ing in Python, so...
		result = Multivector()
		for mask1, coef1 in self.mv.items():
			for mask2, coef2 in other.mv.items():
				coef, mask = Multivector.OP(coef1, mask1, coef2, mask2)
				result.insertBase(coef, mask)
		return result

	@staticmethod
	def OP(coef1: float, mask1: int, coef2: float, mask2: int):
		if (mask1 & mask2 == 0):
			signal = Multivector.CANON_REORDER(mask1, mask2)
			coefResult = signal * coef1 * coef2
			maskResult = mask1 | mask2
			return (coefResult, maskResult)
		else:
			return (0.0, 0)

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
		while (mask != 0):
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


	def removeBase(self, base: int):
		overrideBase(base, 0)

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