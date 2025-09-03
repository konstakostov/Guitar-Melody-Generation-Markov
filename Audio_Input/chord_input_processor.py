from typing import List, Optional
from datasets import load_dataset


class ChordInputProcessor:
    """
    Processes chord sequences from the Chordonomicon dataset.

    Attributes:
        main_genre (Optional[str]): The main genre to filter chord sequences.
        dataset: The loaded Chordonomicon dataset.
        chord_sequences (List[List[str]]): Extracted and filtered chord sequences.

    Methods:
        _extract_chord_sequences() -> List[List[str]]:
            Extracts and filters chord sequences from the dataset, optionally by genre.

        get_available_chords() -> List[str]:
            Returns a sorted list of all unique chords found in the extracted sequences.

        get_dataset_stats() -> dict:
            Returns statistics about the dataset, including total sequences, total chords,
            number of unique chords, and average sequence length.
    """

    def __init__(self, main_genre: Optional[str] = None):
        """
        Initializes the ChordInputProcessor.

        Args:
            main_genre (Optional[str]): If provided, filters chord sequences by this genre.
        """
        print("Loading Chordonomicon dataset...")

        self.dataset = load_dataset("ailsntua/Chordonomicon")
        self.main_genre = main_genre
        self.chord_sequences = self._extract_chord_sequences()

        print(f"Loaded {len(self.chord_sequences)} chord sequences for genre: {self.main_genre or "ALL"}")

    def _extract_chord_sequences(self) -> List[List[str]]:
        """
        Extracts chord sequences from the dataset, filtering by genre if specified.

        Returns:
            List[List[str]]: A list of chord sequences, each sequence is a list of chord strings.
        """
        sequences = []

        for split in self.dataset.keys():
            for item in self.dataset[split]:
                if self.main_genre:
                    item_genre = item.get("main_genre", "")

                    if not isinstance(item_genre, str) or item_genre.lower() != self.main_genre.lower():
                        continue

                if "chords" in item and item["chords"]:
                    if isinstance(item["chords"], list):
                        filtered = [ch for ch in item["chords"] if
                                    ch and isinstance(ch, str) and not ch.startswith("<") and not ch.endswith(">")]

                        sequences.append(filtered)
                    elif isinstance(item["chords"], str):
                        chords = item["chords"].replace(",", " ").split()

                        filtered = [ch for ch in chords if
                                    ch and isinstance(ch, str) and not ch.startswith("<") and not ch.endswith(">")]

                        sequences.append(filtered)

        return [seq for seq in sequences if seq]

    def get_available_chords(self) -> List[str]:
        """
        Returns a sorted list of all unique chords found in the extracted sequences.

        Returns:
            List[str]: Sorted list of unique chord strings.
        """
        all_chords = set()
        for sequence in self.chord_sequences:
            all_chords.update(sequence)

        return sorted(list(all_chords))

    def get_dataset_stats(self) -> dict:
        """
        Returns statistics about the dataset.

        Returns:
            dict: Contains total_sequences, total_chords, unique_chords, and average_length.
        """
        total_sequences = len(self.chord_sequences)
        total_chords = sum(len(seq) for seq in self.chord_sequences)
        unique_chords = len(self.get_available_chords())
        avg_length = total_chords / total_sequences if total_sequences > 0 else 0

        return {
            "total_sequences": total_sequences,
            "total_chords": total_chords,
            "unique_chords": unique_chords,
            "average_length": avg_length
        }
