from OrthogonalMetric import OrthogonalMetric

class Euclidian(OrthogonalMetric):

	def factor(self, bits: int):
		if (bits == 0):
			return 0
		return 1