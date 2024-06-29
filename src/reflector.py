from __future__ import annotations
import json
import random
import string
from dataclasses import dataclass


@dataclass
class ReflectorConfig:
    """
    Configuration for an Enigma machine reflector.

    Attributes:
        name (str): The name of the reflector.
        wiring (str): A 26-character string representing rotor wiring (A-Z).
    """

    wiring: str
    name: str = "Reflector"


class Reflector:
    """
    Represents the reflector of an Enigma machine.

    The reflector is responsible for reversing the electrical signal in the
    Enigma machine, sending it back through the rotors in the opposite direction.
    """

    def __init__(self, config: ReflectorConfig) -> None:
        """
        Initialize a Reflector object.

        Args:
            config (ReflectorConfig): Configuration object containing
                the wiring for the reflector.

        Raises:
            ValueError: If the wiring is not a 26-character string
                with unique letters A-Z.
        """
        self.config = config
        self.wiring = config.wiring
        self.mapping = [ord(c) - ord("A") for c in config.wiring]
        if len(set(self.mapping)) != 26:
            raise ValueError(
                "Wiring must be a 26-character string with unique letters A-Z."
            )

    def reflect(self, input: int) -> int:
        """
        Reflect the input character to a different output character.

        Args:
            input (int): The index of the input character (0-25, where
                0=A, 1=B, ..., 25=Z).

        Returns:
            int: The index of the output character (0-25, where
                0=A, 1=B, ..., 25=Z).
        """
        return self.mapping[input]

    def __call__(self, input: int) -> int:
        """
        Make the Reflector object callable.

        This method simply calls the reflect method.
        """
        return self.reflect(input)

    @staticmethod
    def generate_config() -> ReflectorConfig:
        """
        Generates a ReflectorConfig containing a random 26-character
        string for reflector wiring.
        """
        alphabet = list(string.ascii_uppercase)
        wiring = [""] * 26

        while alphabet:
            a, b = random.sample(alphabet, 2)
            alphabet.remove(a)
            alphabet.remove(b)
            wiring[ord(a) - ord("A")] = b
            wiring[ord(b) - ord("A")] = a

        return ReflectorConfig(wiring="".join(wiring))

    @classmethod
    def load_config(cls, filename: str) -> Reflector:
        """
        Load reflector configs from json file and return a Reflector objects.
        """
        with open(filename, "r") as f:
            data = json.load(f)

        return cls(ReflectorConfig(**data["reflectors"]))

    @staticmethod
    def save_config(config: ReflectorConfig, filename: str):
        """Save a ReflectorConfig object to a json file."""
        if isinstance(config, ReflectorConfig):
            data = {"reflectors": config.__dict__}
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
        else:
            raise TypeError("config must be a RotorConfig object")


if __name__ == "__main__":
    # generate new config
    new_reflector_config = Reflector.generate_config()
    print(
        "New Reflector:",
        new_reflector_config.name,
        new_reflector_config.wiring,
    )

    # save config
    Reflector.save_config(
        new_reflector_config, r"tests/configs/test_reflector_config.json"
    )

    # load config
    reflector = Reflector.load_config(r"tests/configs/test_reflector_config.json")
    print("Loaded rotors:", reflector.wiring)
