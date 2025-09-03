import numpy as np


class MarkovChainSequenceGenerator:
    """
    Generates chord sequences using a Markov chain model with variable-length n-gram context.

    Attributes:
        ngram_loader: An object that provides n-gram transition matrices and mappings.

    Methods:
        generate_sequence(input_sequence, target_length=8):
            Generates a chord sequence of the specified target length, starting from the input_sequence.
            Uses up to 4-gram context for predicting the next chord. If no prediction is possible,
            selects a random chord from the unigram mapping.

        _get_next_chord(window):
            Attempts to predict the next chord using n-gram transition matrices, starting from 4-gram down to unigram.
            Returns the predicted chord or None if no prediction is possible.
    """

    def __init__(self, ngram_loader):
        """
        Initializes the MarkovChainSequenceGenerator.

        Args:
            ngram_loader: An object that provides n-gram transition matrices and mappings.
        """
        self.ngram_loader = ngram_loader

    def generate_sequence(self, input_sequence, target_length=8):
        """
        Generates a chord sequence using Markov chain transitions.

        Args:
            input_sequence (list): Initial sequence of chords.
            target_length (int, optional): Desired length of the output sequence. Defaults to 8.

        Returns:
            list: Generated chord sequence of the specified length.
        """
        sequence = list(input_sequence)
        window_start = 0

        while len(sequence) < target_length:
            window = sequence[window_start:window_start + 4]
            next_chord = self._get_next_chord(window)

            if next_chord is None:
                # Fallback: choose a random chord from the unigram mapping
                _, mapping_1 = self.ngram_loader.get_matrix_and_mapping(1)
                idx_to_chord = mapping_1.get("idx_to_ngram", {})
                next_chord = idx_to_chord[np.random.choice(list(idx_to_chord.keys()))]
            else:
                pass

            sequence.append(next_chord)
            window_start += 1

        return sequence[-target_length:]

    def _get_next_chord(self, window):
        """
        Predicts the next chord using n-gram transition matrices.

        Args:
            window (list): The current context window of chords (up to 4).

        Returns:
            str or None: The predicted next chord, or None if no prediction is possible.
        """
        for n in range(4, 0, -1):
            if len(window) < n:
                continue

            context = tuple(window[:n]) if n > 1 else window[0]
            matrix, mapping = self.ngram_loader.get_matrix_and_mapping(n)

            if matrix is None or mapping is None:
                continue

            ngram_to_idx = mapping.get("ngram_to_idx", {})
            idx_to_ngram = mapping.get("idx_to_ngram", {})
            idx = ngram_to_idx.get(context)

            if idx is None:
                continue

            row = matrix.getrow(idx).toarray().flatten()

            if np.sum(row) == 0:
                continue

            next_idx = np.random.choice(np.arange(len(row)), p=row/row.sum())
            next_ngram = idx_to_ngram[next_idx]

            return next_ngram[-1] if isinstance(next_ngram, tuple) else next_ngram

        return None
