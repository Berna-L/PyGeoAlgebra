from Multivector import Multivector

def decimalToBinary(number):
	string = ""
	count = 0
	while (number > 0):
		count = count + 1
		if (number % 2 == 1):
			if (len(string) > 0):
				string = string + " ^ "
			string = string + "e" + str(count)
		number //= 2
	if (len(string) == 0):
		string = "escalar"
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

result = (e1 + e2 + e3).LCONT(e1)

for mask, coef in sorted(result.mv.items()):
	print("Máscara: ", decimalToBinary(mask), "	Coeficiente: ", coef)

