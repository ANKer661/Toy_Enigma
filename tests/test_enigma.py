import unittest
from src.enigma import EnigmaMachine, EnigmaMachineConfig


class TestEnigmaMachine(unittest.TestCase):
    def setUp(self) -> None:
        """Setup enigma config"""
        self.config = EnigmaMachineConfig()

    def test_encrypt_decrypt(self):
        """Test encryption and decryption"""
        plaintext = "HELLO"
        machine = EnigmaMachine(self.config)
        encrypted = machine.encrypt_decrypt(plaintext)
        machine = EnigmaMachine(self.config)
        decrypted = machine.encrypt_decrypt(encrypted)
        self.assertEqual(decrypted, plaintext)

        plaintext = "HELLOAIOUJOIJQKJLKAJJKCJIAKIOIUQIJLKAJJIOAUSKLQJ"
        machine = EnigmaMachine(self.config)
        encrypted = machine.encrypt_decrypt(plaintext)
        machine = EnigmaMachine(self.config)
        decrypted = machine.encrypt_decrypt(encrypted)
        self.assertEqual(decrypted, plaintext)

        config = EnigmaMachineConfig(
            working_rotor_indices=[4, 2, 1], rotors_init_position=[23, 1, 15]
        )
        plaintext = "HELLOAIOUJOIJQKJLKAJJKCJIAKIOIUQIJLKAJJIOAUSKLQJ"
        machine = EnigmaMachine(config)
        encrypted = machine.encrypt_decrypt(plaintext)
        machine = EnigmaMachine(config)
        decrypted = machine.encrypt_decrypt(encrypted)
        self.assertEqual(decrypted, plaintext)

    def test_choose_rotors(self):
        """Test choosing rotors"""
        machine = EnigmaMachine(self.config)
        machine.choose_rotors(0, 3)
        self.assertEqual(machine.working_rotors[0].name, "Rotor IV")
        machine.choose_rotors(1, 4)
        self.assertEqual(machine.working_rotors[1].name, "Rotor V")

        # choosing an already chosen rotor should raise ValueError
        with self.assertRaises(ValueError) as e:
            machine.choose_rotors(2, 4)
        self.assertIn("has already been chosen", str(e.exception))

    def test_set_rotors_position(self):
        """Test setting rotor positions"""
        machine = EnigmaMachine(self.config)
        machine.set_rotors_position(0, 5)
        self.assertEqual(machine.working_rotors[0]._position, 5)
        machine.set_rotors_position(1, 2)
        self.assertEqual(machine.working_rotors[1]._position, 2)
        machine.set_rotors_position(2, 23)
        self.assertEqual(machine.working_rotors[2]._position, 23)
        # print(machine.get_working_rotors_info())

    def test_set_plugboard(self):
        """Test setting plugboard connections"""
        machine = EnigmaMachine(self.config)
        machine.set_plugboard("AB CD EF")
        self.assertEqual(
            machine.get_plugboard_info(), "Plugboard Connections: AB CD EF"
        )

    def test_rotor_rotation(self):
        """Test rotor rotation pushed by actuator bar"""
        machine = EnigmaMachine(self.config)
        rotors = machine.working_rotors

        # pushing rotors in ActuatorBar
        machine.actuator_bar.push_rotors(rotors)
        positions = [r._position for r in rotors]
        self.assertEqual(positions, [1, 0, 0])

        machine.set_rotors_position(0, rotors[0].notch)
        machine.actuator_bar.push_rotors(rotors)
        positions = [r._position for r in rotors]
        self.assertEqual(positions, [rotors[0].notch + 1, 1, 0])
