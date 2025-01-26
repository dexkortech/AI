import unittest
from classifier import rule_based_classification, hybrid_classification

class TestClassifier(unittest.TestCase):
    def test_rule_based(self):
        self.assertTrue(rule_based_classification("What is AI?"))
        self.assertTrue(rule_based_classification("@bot help me"))
        self.assertFalse(rule_based_classification("Good morning!"))

    def test_hybrid_classification(self):
        self.assertTrue(hybrid_classification("How do neural networks work?"))
        self.assertTrue(hybrid_classification("@bot, what is your purpose?"))
        self.assertFalse(hybrid_classification("Nice weather today!"))

if __name__ == "__main__":
    unittest.main()
