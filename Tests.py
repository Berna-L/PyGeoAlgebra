from Multivector import Multivector
from Clifford import Clifford
import GA

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

def printer(result, description):
	print("\n========================\n", description, "\n========================")
	if (len(result.masks()) is 0):
		print("Multivetor vazio.")
	for mask, coef in sorted(result.items()):
		print("Máscara: ", decimalToBinary(mask), "	Coeficiente: ", coef)


e1 = Multivector.e(1)
e2 = Multivector.e(2)
e3 = Multivector.e(3)
e4 = Multivector.e(4)

#Questão 1
printer(((e1 + e2) ^ (e3 + e2)), "Questão 1a")
printer(((e2 - e1) ^ (e1 - 2 * e3)), "Questão 1b")
printer(((4 * e1 + e2 + e3) ^ (3 * e1)), "Questão 1c")
printer(((e2 + e3) ^ ((0.5 * e1) + e2 + (1.5 * e3))), "Questão 1d")
printer(((e1 + e2) ^ ((e2 ^ e1) + (e3 ^ e2))), "Questão 1e")

#Questão 2
Q2B = e1 ^ (e2 + (2 * e3)) ^ e4

printer(Q2B ^ e1, "Questão 2a")
printer(Q2B ^ (e1 - (3 * e4)), "Questão 2b")
printer(Q2B ^ (e2 + e3), "Questão 2c")

#Questão 3
a = (2 * e2) + e3
b = e2 - e3

printer(a ^ b, "Questão 3")

#Questão 4
a = e1 + e3
b = e1 + e2

metric = Clifford(3, 0, 0)

printer(a * b, "Questão 4a")
printer(GA.LCONT(e3, b, metric), "Questão 4b")
printer(GA.LCONT(e3, a ^ b, metric), "Questão 4c")
printer(GA.LCONT((a ^ b), e1, metric), "Questão 4d")
printer(((2 * a) + b) * (a + b), "Questão 4e")
printer(GA.RCONT((e1 ^ e2 ^ e3), b, metric), "Questão 4f")

#Questão 7

# print("sep=;\n;", end="")
# for i in range(0, 8):
	# print(decimalToBinary(i), ";", end="")
# print("")
# for i in range(0, 8):
# 	mv1 = Multivector()
# 	mv1[i] = 1
# 	# print(decimalToBinary(i), ";", end="")
# 	for j in range(0, 8):
# 		mv2 = Multivector()
# 		mv2[j] = 1
# 		result = GA.GP(mv1, mv2)
# 		printer(result, "Produto geométrico entre " + decimalToBinary(i) + " e " + decimalToBinary(j))

# for i in range(0, 8):
# 	mv1 = Multivector()
# 	mv1[i] = 1
# 	for j in range(0, 8):
# 		mv2 = Multivector()
# 		mv2[j] = 1
# 		result = mv1 ^ mv2
# 		printer(result, "Produto externo entre " + decimalToBinary(i) + " e " + decimalToBinary(j))

# for i in range(0, 8):
# 	mv1 = Multivector()
# 	mv1[i] = 1
# 	for j in range(0, 8):
# 		mv2 = Multivector()
# 		mv2[j] = 1
# 		result = mv1 * mv2
# 		printer(result, "Produto escalar entre blades " + decimalToBinary(i) + " e " + decimalToBinary(j))

# for i in range(0, 8):
# 	mv1 = Multivector()
# 	mv1[i] = 1
# 	for j in range(0, 8):
# 		mv2 = Multivector()
# 		mv2[j] = 1
# 		result = GA.LCONT(mv1, mv2)
# 		printer(result, "Contração à esquerda de " + decimalToBinary(i) + " e " + decimalToBinary(j))

cliff = Clifford(p=2, q=1)

for i in range(0, 8):
	mv1 = Multivector()
	mv1[i] = 1
	for j in range(0, 8):
		mv2 = Multivector()
		mv2[j] = 1
		resultEucl = GA.GP(mv1, mv2)
		resultCliff = GA.GP(mv1, mv2, cliff)
		if (resultEucl == resultCliff):
			print("Produto geométrico entre " + decimalToBinary(i) + " e " + decimalToBinary(j) + " idem euclidiano")
		else:
			printer(resultCliff, "Produto geométrico entre " + decimalToBinary(i) + " e " + decimalToBinary(j))