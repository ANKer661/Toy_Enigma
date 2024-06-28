import unittest
from src.reflector import ReflectorConfig, Reflector


class TestReflector(unittest.TestCase):
    def setUp(self):
        """Initialize a ReflectorConfig object for testing."""
        self.config = ReflectorConfig(wiring="TGJZKVBNLCEIPHXMRQYAWFUOSD")
        self.reflector = Reflector(self.config)

    def test_reflect(self):
        self.assertEqual(
            self.reflector.reflect(ord("T") - ord("A")), ord("A") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("B") - ord("A")), ord("G") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("H") - ord("A")), ord("N") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("D") - ord("A")), ord("Z") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("Z") - ord("A")), ord("D") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("C") - ord("A")), ord("J") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("X") - ord("A")), ord("O") - ord("A")
        )
        self.assertEqual(
            self.reflector.reflect(ord("F") - ord("A")), ord("V") - ord("A")
        )
