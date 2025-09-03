import os
import numpy as np
import pickle

from Utils.path_constants import MATRICES_1_GRAM_PATH, MATRICES_2_GRAM_PATH, MATRICES_3_GRAM_PATH, MATRICES_4_GRAM_PATH


def analyze_matrix_sparsity(genre, n=1):
    """
    Analyze the sparsity characteristics of a transition matrix for a specific genre and n-gram size.

    This function loads a transition matrix for the specified genre and n-gram size, calculates
    various sparsity metrics including density, active elements count, and matrix dimensions.
    It supports both sparse (.npz) and dense (.npy) matrix formats and provides comprehensive
    statistics about the matrix structure.

    Args:
        genre (str): The musical genre to analyze (e.g., 'blues', 'jazz', 'rock').
            Must correspond to an existing matrix file in the appropriate directory.
        n (int, optional): The n-gram size to analyze. Must be in [1, 2, 3, 4].
            Defaults to 1 (unigram/chord-level analysis).

    Returns:
        dict or None: Dictionary containing sparsity analysis results, or None if analysis fails.
            The returned dictionary contains:
            - 'genre': The analyzed genre name
            - 'n': The n-gram size analyzed
            - 'matrix_shape': Tuple of matrix dimensions (rows, cols)
            - 'density': Float representing percentage of non-zero elements (0.0-1.0)
            - 'non_zero_elements': Total count of non-zero matrix elements
            - 'total_elements': Total number of matrix elements (rows × cols)
            - 'active_ngrams': Number of n-grams that have at least one outgoing transition
            - 'total_ngrams': Total number of possible n-grams in the vocabulary
    """
    # Map n-gram sizes to their corresponding directory paths
    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    # Validate the requested n-gram size
    if n not in ngram_paths:
        print(f"Error: Unsupported n-gram size {n}")
        return None

    matrices_path = ngram_paths[n]

    # Check if the directory exists for this n-gram size
    if not os.path.exists(matrices_path):
        print(f"Error: Matrices directory not found for {n}-gram: {matrices_path}")
        return None

    try:
        # Attempt to load sparse matrix format (.npz) first
        matrix_file = os.path.join(matrices_path, f"transition_matrix_{genre}.npz")
        if os.path.exists(matrix_file):
            from scipy.sparse import load_npz
            matrix = load_npz(matrix_file)
            print(f"Loaded {genre} {n}-gram matrix from .npz (sparse)")
        else:
            # Fallback to dense matrix format (.npy)
            matrix_file = os.path.join(matrices_path, f"transition_matrix_{genre}.npy")
            if os.path.exists(matrix_file):
                matrix = np.load(matrix_file)
                print(f"Loaded {genre} {n}-gram matrix from .npy (dense)")
            else:
                print(f"Error: No matrix file found for {genre} {n}-gram")
                return None

        # Load the corresponding n-gram to index mappings
        mappings_file = os.path.join(matrices_path, f"ngram_mappings_{genre}.pkl")
        with open(mappings_file, "rb") as f:
            mappings = pickle.load(f)

        # Calculate sparsity metrics - handle both sparse and dense matrices
        if hasattr(matrix, "todense"):
            # Sparse matrix - use efficient sparse operations
            total_elements = matrix.shape[0] * matrix.shape[1]
            non_zero_elements = matrix.nnz  # Number of non-zero elements in sparse matrix
            density = non_zero_elements / total_elements
        else:
            # Dense matrix - count non-zero elements explicitly
            total_elements = matrix.shape[0] * matrix.shape[1]
            non_zero_elements = np.count_nonzero(matrix)
            density = non_zero_elements / total_elements

        # Count active n-grams (rows with at least one outgoing transition)
        if hasattr(matrix, "todense"):
            # For sparse matrices: sum along axis 1 and count non-zero row sums
            active_ngrams = (matrix.sum(axis=1) > 0).sum()
        else:
            # For dense matrices: sum along axis 1 and count non-zero row sums
            active_ngrams = np.count_nonzero(matrix.sum(axis=1))

        # Compile and return comprehensive sparsity statistics
        return {
            "genre": genre,
            "n": n,
            "matrix_shape": matrix.shape,
            "density": density,
            "non_zero_elements": non_zero_elements,
            "total_elements": total_elements,
            "active_ngrams": int(active_ngrams),
            # Get total vocabulary size from mappings (chord_to_idx for n=1, ngram_to_idx for n>1)
            "total_ngrams": len(mappings.get("ngram_to_idx", mappings.get("chord_to_idx", {})))
        }

    except Exception as e:
        print(f"Error analyzing {genre} {n}-gram matrix: {e}")
        return None
