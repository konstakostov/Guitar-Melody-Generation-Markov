import numpy as np
from scipy.sparse import lil_matrix


def create_transition_matrix(transitions, use_sparse=True, min_count=1):
    """
    Create a probabilistic transition matrix from n-gram transition count data.

    This function takes raw transition counts between n-grams and converts them into
    a normalized transition matrix suitable for Markov chain generation. Each row
    represents the probability distribution of possible next n-grams given the current
    n-gram. The function supports both sparse and dense matrix formats for efficiency.

    Args:
        transitions (dict): Dictionary mapping n-grams to their successor counts.
            Structure: {ngram1: {ngram2: count, ngram3: count, ...}, ...}
            where ngram1 is the current state and ngram2, ngram3 are possible next states.
        use_sparse (bool, optional): Whether to use sparse matrix format for large matrices.
            Automatically switches to sparse format for matrices larger than 10,000x10,000.
            Defaults to True.
        min_count (int, optional): Minimum transition count threshold for inclusion.
            Transitions with counts below this value are filtered out to reduce noise.
            Defaults to 1.

    Returns:
        tuple: A 3-tuple containing:
            - matrix (numpy.ndarray or scipy.sparse matrix): The normalized transition matrix
              where matrix[i,j] represents P(ngram_j | ngram_i). Each row sums to 1.0.
            - ngram_to_idx (dict): Mapping from n-gram strings to matrix row/column indices.
            - idx_to_ngram (dict): Mapping from matrix indices back to n-gram strings.

    Raises:
        ValueError: If transitions is empty, not a dictionary, or contains no valid
            transitions after filtering.
    """
    # Validate input parameters
    if not transitions or not isinstance(transitions, dict):
        raise ValueError("Transitions must be a non-empty dictionary")

    # Filter transitions based on minimum count threshold to reduce noise
    filtered_transitions = {}
    for ngram1, next_ngrams in transitions.items():
        # Skip malformed entries that don't have proper successor dictionaries
        if not isinstance(next_ngrams, dict):
            continue

        # Apply minimum count filtering to reduce noise from rare transitions
        filtered_next = {ng: count for ng, count in next_ngrams.items() if count >= min_count}
        if filtered_next:
            filtered_transitions[ngram1] = filtered_next

    # Build vocabulary from all n-grams present in the filtered data
    all_ngrams = set()
    for ngram1, next_ngrams in filtered_transitions.items():
        # Add the source n-gram to vocabulary
        all_ngrams.add(ngram1)
        # Add all target n-grams to vocabulary
        all_ngrams.update(next_ngrams.keys())

    # Ensure we have valid data after filtering
    if not all_ngrams:
        raise ValueError("No valid n-gram transitions found after filtering")

    # Create bidirectional mappings between n-grams and matrix indices
    # Sort n-grams alphabetically for consistent indexing across runs
    ngram_to_idx = {ngram: idx for idx, ngram in enumerate(sorted(all_ngrams))}
    idx_to_ngram = {idx: ngram for ngram, idx in ngram_to_idx.items()}
    matrix_size = len(all_ngrams)

    print(f"Creating matrix of size {matrix_size}x{matrix_size}")

    # Track whether we're using sparse format for final conversion
    used_sparse = False

    # Choose matrix format based on size and user preference
    if use_sparse and matrix_size > 10000:
        # Use sparse matrix for large vocabularies to save memory
        # LIL (List of Lists) format is efficient for construction
        matrix = lil_matrix((matrix_size, matrix_size))
        used_sparse = True
    else:
        # Use dense matrix for smaller vocabularies or when specifically requested
        matrix = np.zeros((matrix_size, matrix_size))

    # Populate matrix with normalized probabilities
    for ngram1, next_ngrams in filtered_transitions.items():
        row_idx = ngram_to_idx[ngram1]
        # Calculate total count for this n-gram to normalize probabilities
        row_total = sum(next_ngrams.values())

        # Skip n-grams with zero total count (shouldn't happen after filtering)
        if row_total == 0:
            continue

        # Set transition probabilities for each possible next n-gram
        for ngram2, count in next_ngrams.items():
            col_idx = ngram_to_idx[ngram2]
            # Normalize count to probability: P(ngram2 | ngram1) = count / total
            matrix[row_idx, col_idx] = count / row_total

    # Convert sparse matrix to CSR format for efficient operations
    if used_sparse:
        matrix = matrix.tocsr()

    return matrix, ngram_to_idx, idx_to_ngram
