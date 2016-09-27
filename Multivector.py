import collections

class Multivector:

	def __init__(self):
		self.mv = collections.OrderedDict()

	def __add__(self, other):
		result = Multivector()
		done = object()
		iterSelf = iter(self.mv.keys())
		iterOther = iter(other.mv.keys())
		mask1 = next(iterSelf, done)
		mask2 = next(iterOther, done)
		while (mask1 is not done) or (mask2 is not done):
			if (mask1 < mask2):
				result.insertBase(mask1, self.mv[mask1])
				mask1 = next(iterSelf, done)
			elif (mask1 > mask2):
				result.insertBase(mask2, other.mv[mask2])
				mask2 = next(iterOther, done)
			else:
				result.insertBase(mask1, self.mv[mask1] + other.mv[mask2])
				mask1 = next(iterSelf, done)
				mask2 = next(iterOther, done)
		while (mask1 is not done):
			result.insertBase(mask1, self.mv[mask1])
			mask1 = next(iterSelf, done)
		while (mask2 is not done):
			result.insertBase(mask2, other.mv[mask1])
			mask1 = next(iterOther, done)
		return result

	def __radd__(self, other):
		return other + self

	# def __xor__(self, other): #External product, ^ is for xor-ing in Python, so...
	# 	result 

	def insertBase(self, base: int, scale: float):
		if (scale != 0):
			self.mv[base] = scale
		else:
			del self.mv[base]

	def removeBase(self, base: int):
		insertBase(base, 0)