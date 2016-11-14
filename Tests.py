import unittest
from Multivector import Multivector
from Clifford import Clifford
import GA

#Questions based on chapter 2 of Fernandes, Lavor, Oliveira; "Álgebra Geométrica e Aplicações", SMAC,2017

class TestLibraryMethods(unittest.TestCase):

    def test_question_1(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)

        aResult = Multivector()
        aResult[0b011] = 1.0
        aResult[0b101] = 1.0
        aResult[0b110] = 1.0

        self.assertEqual(((e1 + e2) ^ (e3 + e2)), aResult)

        bResult = Multivector()
        bResult[0b011] = -1.0
        bResult[0b101] = 2.0
        bResult[0b110] = -2.0

        self.assertEqual(((e2 - e1) ^ (e1 - 2 * e3)), bResult)

        cResult = Multivector()
        cResult[0b011] = -3.0
        cResult[0b101] = -3.0

        self.assertEqual(((4 * e1 + e2 + e3) ^ (3 * e1)), cResult)

        dResult = Multivector()
        dResult[0b011] = -0.5
        dResult[0b101] = -0.5
        dResult[0b110] = 0.5

        self.assertEqual(((e2 + e3) ^ ((0.5 * e1) + e2 + (1.5 * e3))), dResult)

        eResult = Multivector()
        eResult[0b111] = -1.0

        self.assertEqual(((e1 + e2) ^ ((e2 ^ e1) + (e3 ^ e2))), eResult)

    def test_question_2(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)
        e4 = Multivector.e(4)

        Q2B = e1 ^ (e2 + (2 * e3)) ^ e4

        result = Multivector()

        self.assertEqual(Q2B ^ e1, result)
        self.assertEqual(Q2B ^ (e1 - (3 * e4)), result)

        result[0b1111] = 1.0

        self.assertEqual(Q2B ^ (e2 + e3), result)

    def test_question_3(self):
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)

        a = (2 * e2) + e3
        b = e2 - e3

        result = Multivector()
        result[0b110] = -3.0

        self.assertEqual(a ^ b, result)

    def test_question_4(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)

        a = e1 + e3
        b = e1 + e2

        metric = Clifford(p=3)

        emptyResult = Multivector()

        aResult = Multivector()
        aResult[0b000] = 1.0

        self.assertEqual(a * b, aResult)

        self.assertEqual(GA.LCONT(e3, b, metric), emptyResult)

        cResult = Multivector()
        cResult[0b001] = 1.0
        cResult[0b010] = 1.0

        self.assertEqual(GA.LCONT(e3, a ^ b, metric), cResult)

        self.assertEqual(GA.LCONT((a ^ b), e1, metric), emptyResult)

        eResult = Multivector()
        eResult[0b000] = 9.0

        self.assertEqual(((2 * a) + b) * (a + b), eResult)

        fResult = Multivector()
        fResult[0b101] = -1.0
        fResult[0b110] = 1.0

        self.assertEqual(GA.RCONT((e1 ^ e2 ^ e3), b, metric), fResult)

    def test_reverse(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)

        result = Multivector()
        result[0b111] = -1.0

        self.assertEqual(GA.REVERSE(e1 ^ e2 ^ e3), result)

    def test_inverse(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)

        result = GA.REVERSE(e1 ^ e2 ^ e3)

        self.assertEqual(GA.INVERSE(e1 ^ e2 ^ e3), result)

    def test_dual(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)

        pseudoScalar = GA.INVERSE(e1 ^ e2 ^ e3)
        b = Multivector()
        b[0b011] = 5.0
        b[0b101] = 6.0
        b[0b110] = 7.0

        result = (5.0 *  e3) - (6.0 * e2) + (7.0 * e1)

        self.assertEqual(GA.DUAL(mv=b, dimensions=3), result)

    def test_meet_join(self):
        e1 = Multivector.e(1)
        e2 = Multivector.e(2)
        e3 = Multivector.e(3)
        e4 = Multivector.e(4)

        a = e1 ^ e2 ^ e3
        b = e2 ^ e4

        meetResult = e2
        joinResult = e1 ^ e2 ^ e3 ^ e4

        self.assertEqual(GA.MEET_JOIN(a, b, 4), (meetResult, joinResult))


if __name__ == '__main__':

    unittest.main()
