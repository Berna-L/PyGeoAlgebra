from OrthogonalMetric import OrthogonalMetric

class Clifford(OrthogonalMetric):

	def __init__(self, p, q = 0, r = 0):
		self.p = p
		self.q = q
		self.r = r

	def factor(self, bits: int):
		if (bits == 0):
			return 0
		factor = 1
		i = 0
		while (bits > 0 and i < (self.p + self.q + self.r)):
			if (bits % 2 == 1):
				if (i >= self.p and i < (self.p + self.q)):
					factor = factor * -1
			bits = bits // 2
			i = i + 1
		return factor