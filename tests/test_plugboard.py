import unittest
from src.plugborad import Plugboard


class TestPlugboard(unittest.TestCase):
    def test_valid_connections(self):
        """Test valid connections"""
        pb = Plugboard("AB CD EF")
        self.assertEqual(pb(0), 1)  # A -> B
        self.assertEqual(pb(1), 0)  # B -> A
        self.assertEqual(pb(2), 3)  # C -> D
        self.assertEqual(pb(3), 2)  # D -> C
        self.assertEqual(pb(4), 5)  # E -> F
        self.assertEqual(pb(5), 4)  # F -> E

    def test_case_insensitivity(self):
        """Test case insensitivity"""
        pb = Plugboard("ab CD eF")
        self.assertEqual(pb(0), 1)  # A -> B
        self.assertEqual(pb(1), 0)  # B -> A
        self.assertEqual(pb(2), 3)  # C -> D
        self.assertEqual(pb(3), 2)  # D -> C
        self.assertEqual(pb(4), 5)  # E -> F
        self.assertEqual(pb(5), 4)  # F -> E

    def test_empty_connections(self):
        """Test with no connections"""
        pb = Plugboard("")
        self.assertEqual(pb.mapping, list(range(26)))

    def test_invalid_pair_length(self):
        """Test invalid pair length"""
        with self.assertRaises(ValueError) as context:
            Plugboard("ABC")
        self.assertIn("Invalid connection pair", str(context.exception))

    def test_repeated_character_same_pair(self):
        """Test repeated character in the same pair"""
        with self.assertRaises(ValueError) as context:
            Plugboard("AA")
        self.assertIn("Invalid connection pair", str(context.exception))

    def test_invalid_characters(self):
        """Test invalid characters"""
        with self.assertRaises(ValueError) as context:
            Plugboard("A1")
        self.assertIn("Invalid characters in pair", str(context.exception))

    def test_repeated_character_different_pairs(self):
        """Test repeated character in different pairs"""
        with self.assertRaises(ValueError) as context:
            Plugboard("AB CA")
        err_message = str(context.exception)
        self.assertIn("Repeated character in connections", err_message)
        self.assertTrue(
            "AB" in err_message or "BA" in err_message
        )
        self.assertTrue(
            "AC" in err_message or "CA" in err_message
        )

    def test_multiple_repeated_characters(self):
        """Test multiple repeated characters"""
        with self.assertRaises(ValueError) as context:
            Plugboard("AB CD AD AG")
        err_message = str(context.exception)
        self.assertIn("Repeated character in connections", err_message)
        self.assertTrue(
            "AB" in err_message or "BA" in err_message
        )
        self.assertTrue(
            "DA" in err_message or "AD" in err_message
        )
        self.assertTrue(
            "CD" in err_message or "DC" in err_message
        )
