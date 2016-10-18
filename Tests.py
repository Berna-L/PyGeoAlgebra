from Multivector import Multivector


a = Multivector.e(1)
a.insertBase(1, 0b100)
b = Multivector.e(1)
b.insertBase(1, 0b010)

# for mask, coef in sorted(b.mv.items()):
# 	print("Máscara: ", mask, "Coeficiente: ", coef)

e1 = Multivector.e(1)
e2 = Multivector.e(2)
e3 = Multivector.e(3)

result = b.LCONT(e1 ^ e2 ^ e3)

for mask, coef in sorted(result.mv.items()):
	print("Máscara: ", mask, "Coeficiente: ", coef)