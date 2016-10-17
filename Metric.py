from abc import ABCMeta, abstractmethod

class Metric(metaclass=ABCMeta):

	@abstractmethod
	def factor(self, bits: int):
		pass