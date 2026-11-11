import unittest

from tools.text_stats import summarize


class TextStatsTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(summarize(""), {"lines": 0, "words": 0, "characters": 0})

    def test_two_lines(self):
        self.assertEqual(summarize("Hello world\nGood day\n"), {"lines": 2, "words": 4, "characters": 21})

    def test_unicode(self):
        self.assertEqual(summarize("café ☕"), {"lines": 1, "words": 2, "characters": 6})


if __name__ == "__main__":
    unittest.main()
