from typing import List

from Audio_Input.chord_input_processor import ChordInputProcessor
from Audio_Input.user_input_handler import UserInputHandler
from Audio_Input.random_sequence_generator import RandomSequenceGenerator
from Audio_Input.mixed_sequence_completer import MixedSequenceCompleter

from Utils.get_valid_genre import get_valid_genre


class ChordSequenceController:
    """
    Controls the process of generating and validating chord sequences.

    Attributes:
        processor (ChordInputProcessor): Processes chord data from the dataset.
        input_handler (UserInputHandler): Handles and validates user chord input.
        random_generator (RandomSequenceGenerator): Generates random chord sequences.
        mixed_completer (MixedSequenceCompleter): Completes sequences using mixed strategies.
        sequence (List[str]): Initial chord sequence provided by the user.
        sequence_length (int): Desired length of the chord sequence.

    Methods:
        get_sequence() -> List[str]:
            Returns a valid chord sequence of the specified length.
            If no sequence is provided, generates a random sequence.
            Validates user input and completes the sequence if necessary.
    """

    def __init__(self, sequence: List[str], sequence_length: int, main_genre=None):
        """
        Initializes the ChordSequenceController.

        Args:
            sequence (List[str]): Initial chord sequence.
            sequence_length (int): Desired length of the chord sequence.
            main_genre (str, optional): Main genre to filter chord data.
        """
        if main_genre is not None:
            main_genre = get_valid_genre(main_genre)

        self.processor = ChordInputProcessor(main_genre)
        self.input_handler = UserInputHandler(self.processor)
        self.random_generator = RandomSequenceGenerator(self.processor)
        self.mixed_completer = MixedSequenceCompleter(self.processor)
        self.sequence = sequence
        self.sequence_length = sequence_length

    def get_sequence(self) -> List[str]:
        """
        Returns a valid chord sequence of the specified length.

        If the initial sequence is empty and a length is specified, generates a random sequence.
        Validates the provided sequence and raises an error if invalid chords are found.
        If the sequence is shorter than the desired length, completes it using mixed strategies.

        Returns:
            List[str]: Validated and completed chord sequence.

        Raises:
            ValueError: If invalid chords are found in the input sequence.
        """
        if len(self.sequence) == 0 and self.sequence_length > 0:
            return self.random_generator.get_random_sequence(self.sequence_length)

        valid_chords, invalid_chords = self.input_handler.parse_chord_input(" ".join(self.sequence))

        if invalid_chords:
            raise ValueError(f"Invalid chords: {", ".join(invalid_chords)}")

        if len(self.sequence) >= self.sequence_length:
            return valid_chords[:self.sequence_length]

        return self.mixed_completer.complete_sequence(valid_chords, self.sequence_length)
