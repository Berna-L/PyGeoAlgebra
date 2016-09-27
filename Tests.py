from Multivector import Multivector

mv1 = Multivector()
mv1.insertBase(0b00001, 0.3)
mv2 = Multivector()
mv2.insertBase(0b00001, 2.0)

mvr = mv1 + mv2
print(mvr.mv[0b00001])