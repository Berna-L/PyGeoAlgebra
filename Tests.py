from Multivector import Multivector


mvr = (Multivector.e(2) - Multivector.e(1)) ^ (Multivector.e(1) - Multivector.e_coef(-2, 3))
for mask, coef in sorted(mvr.mv.items()):
	print("Máscara: ", mask, "Coeficiente: ", coef)

mvr2 = (Multivector.e(2) + Multivector.e(3)) ^ (Multivector.e_coef(0.5, 1) + Multivector.e(2) + Multivector.e_coef(1.5, 3))
print("\n\n\n")

for mask, coef in sorted(mvr2.mv.items()):
	print("Máscara: ", mask, "Coeficiente: ", coef)
