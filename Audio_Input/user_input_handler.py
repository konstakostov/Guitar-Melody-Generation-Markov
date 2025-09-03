from typing import List, Tuple

from Audio_Input.chord_input_processor import ChordInputProcessor


class UserInputHandler:
    """
    Handles user input for chord sequences, including validation and parsing.

    Attributes:
        processor (ChordInputProcessor): Provides access to available chords from the dataset.
        available_chords (set): Set of all valid chord symbols.

    Methods:
        validate_chord(chord: str) -> Tuple[bool, str]:
            Validates a single chord symbol against the dataset.

        parse_chord_input(user_input: str) -> Tuple[List[str], List[str]]:
            Parses a user-provided chord sequence string, separating valid and invalid chords.

        get_user_chord_sequence(prompt: str = "Enter chord sequence: ") -> List[str]:
            Prompts the user for a chord sequence, validates input, and returns a list of valid chords.

        suggest_similar_chords(invalid_chord: str, max_suggestions: int = 5) -> List[str]:
            Suggests similar chord symbols from the dataset for an invalid chord.
    """

    def __init__(self, processor: ChordInputProcessor):
        """
        Initializes the UserInputHandler.

        Args:
            processor (ChordInputProcessor): The processor providing available chords.
        """
        self.processor = processor
        self.available_chords = set(processor.get_available_chords())

    def validate_chord(self, chord: str) -> Tuple[bool, str]:
        """
        Validates a single chord symbol.

        Args:
            chord (str): The chord symbol to validate.

        Returns:
            Tuple[bool, str]: (True, "Valid chord") if valid, otherwise (False, error message).
        """
        chord = chord.strip()
        if not chord:
            return False, "Empty chord symbol"

        if chord in self.available_chords:
            return True, "Valid chord"
        else:
            return False, f"Chord '{chord}' not found in dataset"

    def parse_chord_input(self, user_input: str) -> Tuple[List[str], List[str]]:
        """
        Parses a user-provided chord sequence string.

        Args:
            user_input (str): The input string containing chord symbols.

        Returns:
            Tuple[List[str], List[str]]: Lists of valid and invalid chord symbols.
        """
        cleaned_input = user_input.replace(",", " ")
        chord_symbols = [chord.strip() for chord in cleaned_input.split() if chord.strip()]

        valid_chords = []
        invalid_chords = []

        for chord in chord_symbols:
            is_valid, _ = self.validate_chord(chord)
            if is_valid:
                valid_chords.append(chord)
            else:
                invalid_chords.append(chord)

        return valid_chords, invalid_chords

    def get_user_chord_sequence(self, prompt: str = "Enter chord sequence: ") -> list[str] | None:
        """
        Prompts the user for a chord sequence and validates the input.

        Args:
            prompt (str, optional): The prompt message for user input.

        Returns:
            List[str]: List of valid chord symbols entered by the user.
        """
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                print("Please enter at least one chord.")
                continue

            valid_chords, invalid_chords = self.parse_chord_input(user_input)

            if invalid_chords:
                print(f"Invalid chords found: {", ".join(invalid_chords)}")
                print(f"Available chords include: {", ".join(sorted(list(self.available_chords))[:20])}...")
                continue

            if valid_chords:
                return valid_chords
            else:
                print("No valid chords found. Please try again.")

    def suggest_similar_chords(self, invalid_chord: str, max_suggestions: int = 5) -> List[str]:
        """
        Suggests similar chord symbols for an invalid chord.

        Args:
            invalid_chord (str): The invalid chord symbol.
            max_suggestions (int, optional): Maximum number of suggestions to return.

        Returns:
            List[str]: List of suggested similar chord symbols.
        """
        invalid_lower = invalid_chord.lower()
        suggestions = []

        for chord in self.available_chords:
            if invalid_lower in chord.lower() or chord.lower().startswith(invalid_lower):
                suggestions.append(chord)
                if len(suggestions) >= max_suggestions:
                    break

        return suggestions
