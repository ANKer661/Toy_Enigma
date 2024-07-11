from .plugboard import Plugboard
from .reflector import Reflector
from .rotor import Rotor
from dataclasses import dataclass, field


class ActuatorBar:
    """
    Simulates the actuator bar mechanism of an Enigma machine for rotor rotation.

    The ActuatorBar class manages the rotation of rotors based on the
    Enigma machine's stepping mechanism. It checks rotor notch positions
    and rotates them accordingly.
    """

    @staticmethod
    def push_rotors(rotors: list[Rotor]) -> None:
        """
        Pushes the rotor positions based on Enigma machine configuration.

        Args:
            rotors (list[Rotor]): List of rotor objects to push.
        """
        r0, r1, r2 = rotors
        if r1.is_at_notch():
            r1.rotate()
            r2.rotate()
        if r0.is_at_notch():
            r1.rotate()
        r0.rotate()


@dataclass
class EnigmaMachineConfig:
    rotors_config_path: str = r"src/configs/default_rotor_configs.json"
    working_rotor_indices: list[int] = field(default_factory=lambda: [0, 1, 2])
    rotors_init_position: list[int] = field(default_factory=lambda: [0, 0, 0])
    reflector_config_path: str = r"src/configs/default_reflector_config.json"
    plugboard_connections: str = "AJ KU DO WE FC NB QZ GM XV RT"


class EnigmaMachine:
    """
    Simulates an Enigma machine for encryption and decryption of messages.

    This class models an Enigma machine with configurable rotors,
    a reflector, and a plugboard. It supports setting rotor positions,
    plugboard connections, and encrypting/decrypting messages.

    Note:
        Rotor positions:

        +-------------+   +-------------+   +-------------+   +-------------+   +-------------+
        |  reflector  |<--|    rotor2   |<--|    rotor1   |<--|    rotor0   |<--|  plugboard  |
        +-------------+   +-------------+   +-------------+   +-------------+   +-------------+
                                ^                  ^                 ^
                                |                  |                 |
                        positions = 2      positions = 1     positions = 0
    """

    def __init__(self, enigma_config: EnigmaMachineConfig) -> None:
        """
        Initializes the Enigma machine with default components and settings.
        """
        # We have 5 rotors
        self.config = enigma_config
        self.rotors = Rotor.load_config(self.config.rotors_config_path)

        # Choose 3 rotors for encryption and decryption
        self.working_rotor_indices = self.config.working_rotor_indices
        # Initialize working rotors and set their initial positions
        self.working_rotors = [
            self.rotors[i].set_position(pos)
            for i, pos in zip(
                self.working_rotor_indices, self.config.rotors_init_position
            )
        ]

        self.reflector = Reflector.load_config(self.config.reflector_config_path)
        self.plugboard = Plugboard(
            self.config.plugboard_connections
        )
        self.actuator_bar = ActuatorBar()

        self.update_circuit()

    def update_circuit(self):
        """
        Updates the Enigma machine's circuit configuration based on current settings.
        """
        self.circuit = [
            self.plugboard,
            *self.working_rotors,
            self.reflector,
            *[rotor.backward for rotor in reversed(self.working_rotors)],
            self.plugboard,
        ]

    def encrypt_decrypt(self, message: str) -> str:
        """
        Encrypts or decrypts a message using the current Enigma machine settings.

        Args:
            message (str): The message to encrypt or decrypt.

        Returns:
            str: The encrypted or decrypted message.
        """
        ciphertext = ""
        for letter in message:
            self.actuator_bar.push_rotors(self.working_rotors)
            current_letter = letter

            for component in self.circuit:
                current_letter = component(current_letter)

            ciphertext += chr(ord("A") + current_letter)

        return ciphertext

    def __call__(self, message: str) -> str:
        """
        Make Enigma Machine callable.

        Simply call the encrypt_decrypt method.
        """
        return self.encrypt_decrypt(message)

    def choose_rotors(
        self,
        target_rotor_indices: list[int],
        init_positions: list[int] | None = None,
    ) -> None:
        """
        Choose a rotor at a specific position in the Enigma
        machine configuration.

        Args:
            target_rotor_indices (int): A list of the indices of the
                rotor to be placed at the specified positions.
            init_positions (list[int]): A list of the initial position
                of the new rotor.
        """
        if init_positions is None:
            init_positions = [0, 0, 0]
        self.working_rotors = [
            self.rotors[i].set_position(pos)
            for i, pos in zip(target_rotor_indices, init_positions)
        ]

    def set_rotors_position(self, working_rotor_position: int, rotor_position: int):
        """
        Sets the position of a rotor in the Enigma machine.

        Args:
            working_rotor_position (int): The position in the rotor chain
                where the rotor position is set.
            rotor_position (int): The new position of the rotor (0-25).
        """
        self.working_rotors[working_rotor_position].set_position(rotor_position % 26)

    def set_plugboard(self, connections: str | None = None) -> None:
        """
        Sets the plugboard connections for the Enigma machine.

        See details in Plugboard.set_plugboard() of src/plugboard.py

        Args:
            connections (str, optional): A string representing plugboard
                connections as letter pairs.
        """
        self.plugboard.set_plugboard(connections)

    def get_working_rotors_position(self) -> list[int]:
        """
        Retrieves current position of the current working rotors.

        Returns:
            list[int]: A list of each working rotor's current position.
        """
        return [rotor.get_current_position() for rotor in self.working_rotors]

    def get_working_rotors_info(self) -> str:
        """
        Retrieves information about the current working rotors.

        Returns:
            str: A string describing each working rotor's
                configuration and current position.
        """
        return "\n".join([str(rotor) for rotor in self.working_rotors])

    def get_reflector_info(self) -> str:
        """
        Retrieves information about the reflector configuration.

        Returns:
            str: A string representing the current reflector configuration.
        """
        return str(self.reflector)

    def get_plugboard_info(self) -> str:
        """
        Retrieves information about the current plugboard connections.

        Returns:
            str: A string representing the current plugboard connections.
        """
        return str(self.plugboard)

    def get_enigma_info(self) -> str:
        """
        Retrieves detailed information about the Enigma machine.

        Returns:
            str: A string containing information about the current Enigma
                machine configuration, including rotor settings,
                reflector configuration, and plugboard connections.
        """
        rotor_info = self.get_working_rotors_info()
        reflector_info = self.get_reflector_info()
        plugboard_info = self.get_plugboard_info()

        return (
            "Enigma Machine Configuration:  \n\n"
            f"{rotor_info}  \n\n"
            f"{reflector_info}  \n\n"
            f"{plugboard_info}  \n"
        )


def generate_configs() -> None:
    """
    Generates and saves new rotor and reflector configurations to files.
    """
    # Generate new rotor configurations
    rotor_config = [
        Rotor.generate_config(f"Rotor {i}") for i in ["I", "II", "III", "IV", "V"]
    ]

    # Save rotor configurations to a file
    Rotor.save_config(rotor_config, r"src/configs/default_rotor_configs.json")

    # Load rotor configurations from the file
    loaded_rotors = Rotor.load_config(r"src/configs/default_rotor_configs.json")
    print("Loaded rotors:", *[(r.name, r.wiring, r.notch) for r in loaded_rotors])

    # Generate a new reflector configuration
    reflector_config = Reflector.generate_config()

    # Save reflector configuration to a file
    Reflector.save_config(
        reflector_config, r"src/configs/default_reflector_config.json"
    )

    # Load reflector configuration from the file
    reflector = Reflector.load_config(r"src/configs/default_reflector_config.json")
    print("Loaded reflector:", reflector.wiring)


if __name__ == "__main__":
    # generate_configs()
    pass
