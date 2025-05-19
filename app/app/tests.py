from django.test import SimpleTestCase

from . import calc


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_sub_nums(self):
        res = calc.subtract(6, 5)
        self.assertEqual(res, 1)
