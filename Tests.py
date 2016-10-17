from Multivector import Multivector


a = Multivector.e(1)
a.insertBase(1, 0b100)
b = Multivector.e(1)
b.insertBase(1, 0b010)

for mask, coef in sorted(b.mv.items()):
	print("Máscara: ", mask, "Coeficiente: ", coef)

result = Multivector.e(3).LCONT(b)

for mask, coef in sorted(result.mv.items()):
	print("Máscara: ", mask, "Coeficiente: ", coef)