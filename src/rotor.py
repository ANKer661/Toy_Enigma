import json
import random
import string
from dataclasses import dataclass


@dataclass
class RotorConfig:
    """
    Configuration for an Enigma machine rotor.

    Attributes:
        name (str): The name of the rotor.
        wiring (str): A 26-character string representing rotor wiring (A-Z).
        notch (int): Notch position (0-25, where 0=A, 1=B, ..., 25=Z).
    """

    name: str
    wiring: str
    notch: int


class Rotor:
    """
    Represents a rotor in an Enigma machine.

    Rotors perform letter substitution and rotate with each keypress,
    forming the core of Enigma's encryption mechanism.
    """

    def __init__(self, config: RotorConfig, init_position: int = 0) -> None:
        """
        Initializes the Rotor with the given configuration
        and initial position.

        Args:
            config (RotorConfig): The configuration for the rotor.
            init_position (int): The initial position of the rotor (default 0).
        """
        self._position = init_position
        self.name = config.name
        self.wiring = config.wiring
        self.notch = config.notch

        self.forward_mapping = [ord(c) - ord("A") for c in self.wiring]
        self.backward_mapping = [0] * 26
        for i, c in enumerate(self.wiring):
            self.backward_mapping[ord(c) - ord("A")] = i

        self.direction_methods = {"forward": self.forward, "backward": self.backward}

    def forward(self, input: int) -> int:
        """
        Maps the input character index through the rotor's wiring in
        the forward direction.

        Args:
            input (int): The index of the input character (0-25, where
                0=A, 1=B, ..., 25=Z).

        Returns:
            int: The index of the output character after passing
                through the rotor in forward direction.
        """
        index = (self._position + input) % 26
        output = self.forward_mapping[index]
        return (output - self._position + 26) % 26

    def backward(self, input: int) -> int:
        """
        Maps the input character index through the rotor's wiring
        in the backward direction.

        Args:
            input (int): The index of the input character (0-25, where
                0=A, 1=B, ..., 25=Z).

        Returns:
            int: The index of the output character after passing
                through the rotor in the backward direction.
        """
        index = (self._position + input) % 26
        output = self.backward_mapping[index]
        return (output - self._position + 26) % 26

    def __call__(self, input: int, direction: str = "forward") -> int:
        if direction not in self.direction_methods:
            raise ValueError("Direction must be either 'forward' or 'backward'")

        return self.direction_methods[direction](input)

    def rotate(self) -> None:
        """Rotates the rotor by one position."""
        self._position = (self._position + 1) % 26

    def set_position(self, position: int) -> None:
        """Sets the rotor to a specific position."""
        self._position = position

    def is_at_notch(self) -> bool:
        """
        Checks if the rotor is at the notch position.

        Returns:
            bool: True if the rotor is at the notch position, False otherwise.
        """
        return self._position == self.notch

    @staticmethod
    def generate_config(name: str) -> RotorConfig:
        """Generate a random rotor config."""
        alphabet = list(string.ascii_uppercase)
        random.shuffle(alphabet)
        wiring = "".join(alphabet)
        notch = random.randint(0, 25)

        return RotorConfig(name=name, wiring=wiring, notch=notch)

    @staticmethod
    def load_config(filename: str) -> "list[Rotor]":
        """
        Load rotor configs from json file and return a list of Rotor objects.
        """
        with open(filename, "r") as f:
            data = json.load(f)
        return [Rotor(RotorConfig(**rotor_data)) for rotor_data in data["rotors"]]

    @staticmethod
    def save_config(configs: RotorConfig | list[RotorConfig], filename: str):
        """Save a list of RotorConfig objects to a json file."""
        if isinstance(configs, RotorConfig):
            configs = [configs]
        elif isinstance(configs, list):
            if not all(isinstance(config, RotorConfig) for config in configs):
                raise TypeError("All elements in the list must be RotorConfig objects")
        else:
            raise TypeError(
                "configs must be a RotorConfig object or a list of RotorConfig objects"
            )

        data = {"rotors": [config.__dict__ for config in configs]}
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    # generate new config
    new_rotor_config = Rotor.generate_config("Rotor I")
    print(
        "New rotor:",
        new_rotor_config.name,
        new_rotor_config.wiring,
        new_rotor_config.notch,
    )

    # save config
    Rotor.save_config(new_rotor_config, r"tests/configs/test_rotor_configs.json")

    # load config
    loaded_rotors = Rotor.load_config(r"tests/configs/test_rotor_configs.json")
    print("Loaded rotors:", *[(r.name, r.wiring, r.notch) for r in loaded_rotors])
