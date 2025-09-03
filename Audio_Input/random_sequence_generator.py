import random
from typing import List

from Audio_Input.chord_input_processor import ChordInputProcessor

class RandomSequenceGenerator:
    """
    Generates random chord sequences from a dataset of chord progressions.

    Attributes:
        processor (ChordInputProcessor): Provides access to chord sequences from the dataset.

    Methods:
        get_random_sequence(length: int) -> List[str]:
            Returns a random chord sequence of the specified length.
            If no sequence of sufficient length exists, concatenates random sequences.

        _concatenate_random_sequences(length: int) -> List[str]:
            Concatenates random sequences until the desired length is reached.

        get_random_chord() -> str:
            Returns a single random chord from the dataset.

        get_multiple_random_sequences(count: int, length: int) -> List[List[str]]:
            Returns a list of random chord sequences, each of the specified length.
    """

    def __init__(self, processor: ChordInputProcessor):
        """
        Initializes the RandomSequenceGenerator.

        Args:
            processor (ChordInputProcessor): The processor containing chord sequences.
        """
        self.processor = processor

    def get_random_sequence(self, length: int) -> List[str]:
        """
        Returns a random chord sequence of the specified length.

        If no sequence of sufficient length exists, concatenates random sequences.

        Args:
            length (int): Desired length of the chord sequence.

        Returns:
            List[str]: A random chord sequence.

        Raises:
            ValueError: If no chord sequences are available or length is not positive.
        """
        if not self.processor.chord_sequences:
            raise ValueError("No chord sequences available in dataset")

        if length <= 0:
            raise ValueError("Length must be positive")

        suitable_sequences = [seq for seq in self.processor.chord_sequences if len(seq) >= length]

        if not suitable_sequences:
            return self._concatenate_random_sequences(length)

        chosen_sequence = random.choice(suitable_sequences)

        if len(chosen_sequence) == length:
            return chosen_sequence

        start_idx = random.randint(0, len(chosen_sequence) - length)

        return chosen_sequence[start_idx:start_idx + length]

    def _concatenate_random_sequences(self, length: int) -> List[str]:
        """
        Concatenates random sequences until the desired length is reached.

        Args:
            length (int): Desired total length of the concatenated sequence.

        Returns:
            List[str]: Concatenated chord sequence of the specified length.
        """
        result = []

        while len(result) < length:
            random_seq = random.choice(self.processor.chord_sequences)
            result.extend(random_seq)

        return result[:length]

    def get_random_chord(self) -> str:
        """
        Returns a single random chord from the dataset.

        Returns:
            str: A random chord.

        Raises:
            ValueError: If no chord sequences are available.
        """
        all_sequences = self.processor.chord_sequences

        if not all_sequences:
            raise ValueError("No chord sequences available")

        random_sequence = random.choice(all_sequences)

        return random.choice(random_sequence)

    def get_multiple_random_sequences(self, count: int, length: int) -> List[List[str]]:
        """
        Returns a list of random chord sequences, each of the specified length.

        Args:
            count (int): Number of sequences to generate.
            length (int): Length of each sequence.

        Returns:
            List[List[str]]: List of random chord sequences.
        """
        return [self.get_random_sequence(length) for _ in range(count)]
