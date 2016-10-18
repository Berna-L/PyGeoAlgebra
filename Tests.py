from Multivector import Multivector

def decimalToBinary(number):
	string = ""
	while (number > 0):
		string = string + str(number % 2)
		number //= 2
	return string

a = Multivector.e(1)
a.insertBase(1, 0b100)
b = Multivector.e(1)
b.insertBase(1, 0b010)

# for mask, coef in sorted(b.mv.items()):
# 	print("Máscara: ", mask, "Coeficiente: ", coef)

e1 = Multivector.e(1)
e2 = Multivector.e(2)
e3 = Multivector.e(3)

result = e3.LCONT(a ^ b)

for mask, coef in sorted(result.mv.items()):
	print("Máscara: ", decimalToBinary(mask), "Coeficiente: ", coef)

