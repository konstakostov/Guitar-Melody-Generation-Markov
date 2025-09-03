from typing import List
import random

from Audio_Input.chord_input_processor import ChordInputProcessor
from Audio_Input.random_sequence_generator import RandomSequenceGenerator


class MixedSequenceCompleter:
    """
    Completes a chord sequence to a target length using a mix of dataset transitions and random selection.

    Attributes:
        processor (ChordInputProcessor): Processes chord data from the dataset.
        transition_map (dict): Maps each chord to possible next chords based on dataset transitions.

    Methods:
        complete_sequence(start_sequence: List[str], target_length: int) -> List[str]:
            Extends the start_sequence to the target_length using learned transitions and random chords.
    """

    def __init__(self, processor: ChordInputProcessor):
        """
        Initializes the MixedSequenceCompleter.

        Args:
            processor (ChordInputProcessor): The processor containing chord sequences and available chords.
        """
        self.processor = processor
        self.transition_map = self._build_transition_map()

    def _build_transition_map(self):
        """
        Builds a transition map from the dataset, mapping each chord to possible next chords.

        Returns:
            dict: A dictionary where keys are chords and values are lists of possible next chords.
        """
        transitions = {}

        for sequence in self.processor.chord_sequences:
            for i in range(len(sequence) - 1):
                curr, nxt = sequence[i], sequence[i + 1]
                transitions.setdefault(curr, []).append(nxt)

        return transitions

    def complete_sequence(self, start_sequence: List[str], target_length: int) -> List[str]:
        """
        Completes a chord sequence to the specified target length.

        If the start_sequence is empty, generates a random sequence.
        Otherwise, extends the sequence using the transition map; if no transition is found,
        selects a random chord from available chords.

        Args:
            start_sequence (List[str]): The initial chord sequence.
            target_length (int): The desired length of the completed sequence.

        Returns:
            List[str]: The completed chord sequence of the specified length.
        """
        if not start_sequence:
            return RandomSequenceGenerator(self.processor).get_random_sequence(target_length)

        result = list(start_sequence)

        while len(result) < target_length:
            last_chord = result[-1]
            next_chords = self.transition_map.get(last_chord)

            if next_chords:
                result.append(random.choice(next_chords))
            else:
                result.append(random.choice(self.processor.get_available_chords()))

        return result[:target_length]
