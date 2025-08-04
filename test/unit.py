import unittest

def func(x):
    return x + 1

class TestFunc(unittest.TestCase):
    def test_answer_1(self):
        self.assertEqual(func(3), 4)

    def test_answer_2(self):
        self.assertEqual(func(4), 5)

    def test_answer_3(self):
        self.assertEqual(func(5), 6)

if __name__ == '__main__':
    unittest.main()
