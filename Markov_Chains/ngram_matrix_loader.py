import os
import pickle
from scipy.sparse import load_npz

from Utils.path_constants import MATRICES_1_GRAM_PATH, MATRICES_2_GRAM_PATH, MATRICES_3_GRAM_PATH, MATRICES_4_GRAM_PATH


class NGramMatrixLoader:
    """
    Loads n-gram transition matrices and their mappings for a given genre.

    Attributes:
        genre (str): The genre for which matrices and mappings are loaded.
        ngram_paths (dict): Maps n-gram order (1-4) to their respective directory paths.
        matrices (dict): Stores loaded transition matrices for each n-gram order.
        mappings (dict): Stores loaded n-gram mappings for each n-gram order.

    Methods:
        get_matrix_and_mapping(n):
            Returns the transition matrix and mapping for the specified n-gram order.
    """

    def __init__(self, genre):
        """
        Initializes the NGramMatrixLoader for a specific genre.

        Args:
            genre (str): The genre to load matrices and mappings for.
        """
        self.genre = genre
        self.ngram_paths = {
            1: MATRICES_1_GRAM_PATH,
            2: MATRICES_2_GRAM_PATH,
            3: MATRICES_3_GRAM_PATH,
            4: MATRICES_4_GRAM_PATH
        }
        self.matrices = {}
        self.mappings = {}
        self._load_all_matrices()

    def _load_all_matrices(self):
        """
        Loads all available n-gram transition matrices and mappings for the specified genre.
        If a matrix or mapping file does not exist, sets the corresponding entry to None.
        """
        for n in range(1, 5):
            matrices_path = self.ngram_paths[n]
            matrix_file = os.path.join(matrices_path, f"transition_matrix_{self.genre}.npz")
            mappings_file = os.path.join(matrices_path, f"ngram_mappings_{self.genre}.pkl")

            if os.path.exists(matrix_file) and os.path.exists(mappings_file):
                self.matrices[n] = load_npz(matrix_file)
                with open(mappings_file, "rb") as f:
                    self.mappings[n] = pickle.load(f)
            else:
                self.matrices[n] = None
                self.mappings[n] = None

    def get_matrix_and_mapping(self, n):
        """
        Retrieves the transition matrix and mapping for the specified n-gram order.

        Args:
            n (int): The n-gram order (1, 2, 3, or 4).

        Returns:
            tuple: (matrix, mapping) for the given n-gram order, or (None, None) if not available.
        """
        return self.matrices.get(n), self.mappings.get(n)
