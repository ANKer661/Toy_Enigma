class Plugboard:
    """
    Represents the plugboard of an Enigma machine.

    The plugboard allows for additional letter substitutions
    before and after the rotor.
    """

    def __init__(self, connections: str | None = None) -> None:
        """
        Initialize the plugboard with given connections.

        Args:
            connections (str): A string of space-separated letter pairs representing
                               the plugboard connections.
                               E.g., "AB CD EF" connects A to B, C to D, E to F.
                               If not provided, default connections will be used.

        Raises:
            ValueError: If more than 10 connections are provided
                        or if any connection pair is invalid,
                        if any character is used more than once,
                        or if any pair contains invalid characters.
        """
        if connections is None:
            connections = "AJ KU DO WE FC NB QZ GM XV RT"

        connection_pairs = connections.split()
        if len(connection_pairs) > 10:
            raise ValueError("Only up to 10 connections are supported.")

        self.mapping = list(range(26))
        for pair in connection_pairs:
            if len(pair) != 2:
                raise ValueError(f"Invalid connection pair: {pair}")

            char1, char2 = pair
            index1 = ord(char1.upper()) - ord("A")
            index2 = ord(char2.upper()) - ord("A")

            if index1 == index2:
                raise ValueError(f"Invalid connection pair: {pair}")

            if not (0 <= index1 < 26 and 0 <= index2 < 26):
                raise ValueError(f"Invalid characters in pair: {pair}")

            if self.mapping[index1] != index1 or self.mapping[index2] != index2:
                duplicates = [pair]
                if self.mapping[index1] != index1:
                    duplicates.append(
                        chr(ord("A") + index1) + chr(ord("A") + self.mapping[index1])
                    )
                if self.mapping[index2] != index2:
                    duplicates.append(
                        chr(ord("A") + index2) + chr(ord("A") + self.mapping[index2])
                    )
                raise ValueError(
                    f"Repeated character in connections: {', '.join(duplicates)}"
                )

            self.mapping[index1] = index2
            self.mapping[index2] = index1

    def pass_through(self, input: int | str) -> int:
        """
        Pass a character through the plugboard.

        Args:
            input (int | str): Either an integer index (0-25)
                or a single character (A-Z).

        Returns:
            int: The index of the output character after passing through the plugboard.
        """
        if isinstance(input, str):
            input = ord(input.upper()) - ord("A")

        return self.mapping[input]

    def __call__(self, input: int | str) -> int:
        """
        Make Plugboard callable.

        This method simply calls the pass_through method.
        """
        return self.pass_through(input)

    def reset(self) -> None:
        """Reset the plugboard state to no connections."""
        self.mapping = list(range(26))
