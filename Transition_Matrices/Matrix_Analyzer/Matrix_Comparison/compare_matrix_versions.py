import os
import numpy as np
import pickle
from scipy.sparse import load_npz

from Utils.path_constants import MATRICES_1_GRAM_PATH, MATRICES_2_GRAM_PATH, MATRICES_3_GRAM_PATH, MATRICES_4_GRAM_PATH

def compare_matrix_versions(genre, n1=1, n2=2):
    """
    Compares two n-gram transition matrices for a given genre and n-gram sizes.

    Loads the matrices and their mappings, calculates metrics such as size, density,
    and element counts, and returns a summary dictionary.

    Args:
        genre (str): The genre to compare matrices for.
        n1 (int, optional): The first n-gram size to compare. Defaults to 1.
        n2 (int, optional): The second n-gram size to compare. Defaults to 2.

    Returns:
        dict or None: Dictionary containing comparison metrics, or None if an error occurs.
    """
    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    if n1 not in ngram_paths or n2 not in ngram_paths:
        print(f"Error: Unsupported n-gram sizes {n1} or {n2}")
        return None

    try:
        # Load matrices and mappings
        matrix1, mappings1 = _load_matrix_and_mappings(genre, n1, ngram_paths)
        matrix2, mappings2 = _load_matrix_and_mappings(genre, n2, ngram_paths)

        # Calculate metrics
        size1 = matrix1.shape[0] * matrix1.shape[1]
        size2 = matrix2.shape[0] * matrix2.shape[1]

        # Handle both dense and sparse matrices for density calculation
        if hasattr(matrix1, "nnz"):
            density1 = matrix1.nnz / size1
        else:
            density1 = np.count_nonzero(matrix1) / size1

        if hasattr(matrix2, "nnz"):
            density2 = matrix2.nnz / size2
        else:
            density2 = np.count_nonzero(matrix2) / size2

        element_type1 = "chords" if n1 == 1 else f"{n1}-grams"
        element_type2 = "chords" if n2 == 1 else f"{n2}-grams"

        return {
            "genre": genre,
            "n1": n1,
            "n2": n2,
            "size1": size1,
            "size2": size2,
            "size_change": (size2 - size1) / size1,
            "density1": density1,
            "density2": density2,
            "density_change": (density2 - density1) / density1 if density1 > 0 else 0,
            "elements1_count": len(mappings1.get("ngram_to_idx", mappings1.get("chord_to_idx", {}))),
            "elements2_count": len(mappings2.get("ngram_to_idx", mappings2.get("chord_to_idx", {}))),
            "element_type1": element_type1,
            "element_type2": element_type2
        }

    except Exception as e:
        print(f"Error comparing {genre} matrices ({n1}-gram vs {n2}-gram): {e}")
        return None


def compare_all_adjacent_ngrams(genre):
    """
    Compares all adjacent n-gram sizes (1-gram to 4-gram) for a given genre.

    Finds available n-gram sizes for the genre, then compares each adjacent pair
    using `compare_matrix_versions`.

    Args:
        genre (str): The genre to compare matrices for.

    Returns:
        list: List of comparison dictionaries for each adjacent n-gram pair.
    """
    ngram_sizes = [1, 2, 3, 4]
    available_sizes = []

    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    # Find which n-gram sizes are available for this genre
    for n in ngram_sizes:
        matrix_file = os.path.join(ngram_paths[n], f"transition_matrix_{genre}.npz")
        if os.path.exists(matrix_file):
            available_sizes.append(n)

    if len(available_sizes) < 2:
        return []

    comparisons = []

    for i in range(len(available_sizes) - 1):
        comparison = compare_matrix_versions(genre, available_sizes[i], available_sizes[i + 1])
        if comparison:
            comparisons.append(comparison)

    return comparisons


def _load_matrix_and_mappings(genre, n, ngram_paths):
    """
    Loads the transition matrix and mappings for a given genre and n-gram size.

    Handles both sparse (.npz) and dense (.npy) matrix formats.

    Args:
        genre (str): The genre to load data for.
        n (int): The n-gram size.
        ngram_paths (dict): Mapping of n-gram sizes to their directory paths.

    Returns:
        tuple: (matrix, mappings) where matrix is the transition matrix and mappings is the n-gram mapping dictionary.
    """
    matrices_path = ngram_paths[n]

    # Try .npz first (sparse format)
    matrix_file = os.path.join(matrices_path, f"transition_matrix_{genre}.npz")

    if os.path.exists(matrix_file):
        matrix = load_npz(matrix_file)
    else:
        # Fallback to .npy (dense format)
        matrix_file = os.path.join(matrices_path, f"transition_matrix_{genre}.npy")
        matrix = np.load(matrix_file)

    # Load mappings
    mappings_file = os.path.join(matrices_path, f"ngram_mappings_{genre}.pkl")

    with open(mappings_file, "rb") as f:
        mappings = pickle.load(f)

    return matrix, mappings
