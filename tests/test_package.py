import unittest

from wavebench.data.package import safe_label


class PackageTests(unittest.TestCase):
    def test_safe_label_keeps_simple_names(self):
        self.assertEqual(safe_label("ch1"), "ch1")

    def test_safe_label_replaces_spaces(self):
        self.assertEqual(safe_label("my capture"), "my_capture")


if __name__ == "__main__":
    unittest.main()
