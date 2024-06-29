import unittest
from src.rotor import Rotor, RotorConfig


class TestRotor(unittest.TestCase):
    def setUp(self):
        """Initialize a RotorConfig object for testing."""
        self.config = RotorConfig(
            name="Test Rotor", wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch=17
        )

    def test_rotate(self):
        """Test rotor rotation."""
        self.rotor = Rotor(self.config, init_position=0)
        for i in range(1, 30):
            self.rotor.rotate()
            self.assertEqual(self.rotor._position, i % 26)

    def test_forward(self):
        """Test forward mapping."""
        self.rotor = Rotor(self.config, init_position=0)
        self.assertEqual(self.rotor.forward(0), (ord("E") - ord("A")))
        self.rotor.rotate()
        self.assertEqual(self.rotor.forward(0), (ord("K") - ord("A")) - 1)
        self.rotor.rotate()
        self.assertEqual(self.rotor.forward(0), (ord("M") - ord("A")) - 2)

    def test_backward(self):
        """Test backward mapping."""
        self.rotor = Rotor(self.config, init_position=0)
        self.assertEqual(self.rotor.backward(ord("E") - ord("A")), 0)
        self.assertEqual(self.rotor.backward(ord("L") - ord("A")), 4)
        self.rotor.rotate()
        self.assertEqual(self.rotor.backward(ord("E") - ord("A")), 2)
        self.assertEqual(self.rotor.backward(ord("F") - ord("A")), 4)

    def test_call(self):
        """Test __call__ method."""
        self.rotor = Rotor(self.config, init_position=0)
        self.assertEqual(self.rotor(0), (ord("E") - ord("A")))
        self.rotor.rotate()
        self.assertEqual(self.rotor(0), (ord("K") - ord("A")) - 1)
        self.rotor.rotate()
        self.assertEqual(self.rotor(0), (ord("M") - ord("A")) - 2)

        self.rotor = Rotor(self.config, init_position=0)
        self.assertEqual(self.rotor(ord("E") - ord("A"), "backward"), 0)
        self.assertEqual(self.rotor(ord("L") - ord("A"), "backward"), 4)
        self.rotor.rotate()
        self.assertEqual(self.rotor(ord("E") - ord("A"), "backward"), 2)
        self.assertEqual(self.rotor(ord("F") - ord("A"), "backward"), 4)

    def test_set_position(self):
        """Test setting rotor position."""
        self.rotor = Rotor(self.config, init_position=0)
        self.rotor.set_position(5)
        self.assertEqual(self.rotor._position, 5)
        self.rotor.set_position(23)
        self.assertEqual(self.rotor._position, 23)

    def test_is_at_notch(self):
        """Test if the rotor is at the notch position."""
        self.rotor = Rotor(self.config, init_position=0)
        self.rotor.set_position(12)
        self.assertFalse(self.rotor.is_at_notch())
        self.rotor.set_position(17)
        self.assertTrue(self.rotor.is_at_notch())
        self.rotor.rotate()
        self.assertFalse(self.rotor.is_at_notch())
