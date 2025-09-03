import os
import numpy as np

from Transition_Matrices.Matrix_Analyzer.Sparsity_Analyzer.analyze_matrix_sparsity import analyze_matrix_sparsity
from Utils.path_constants import MATRICES_1_GRAM_PATH, MATRICES_2_GRAM_PATH, MATRICES_3_GRAM_PATH, MATRICES_4_GRAM_PATH


def analyze_all_matrices(ngram_sizes=None):
    """
    Analyze sparsity characteristics of all available transition matrices across n-gram sizes.

    This function scans directories for each specified n-gram size, identifies available genre
    matrices, and performs sparsity analysis on each one. It provides a comprehensive report
    showing matrix dimensions, density percentages, and active element counts for each genre
    and n-gram size combination.

    Args:
        ngram_sizes (list of int, optional): List of n-gram sizes to analyze. Must be values
            from [1, 2, 3, 4]. Defaults to [1, 2, 3, 4] if not specified.

    Returns:
        dict: Dictionary mapping n-gram sizes (int) to lists of statistics dictionaries.
            Each statistics dictionary contains:
            - 'genre': Name of the musical genre
            - 'matrix_shape': Tuple of matrix dimensions (rows, cols)
            - 'density': Float representing the percentage of non-zero elements (0.0-1.0)
            - 'active_ngrams': Number of n-grams with at least one transition
            - 'total_ngrams': Total number of possible n-grams in the matrix
            - 'sparsity': Float representing the percentage of zero elements (0.0-1.0)
    """
    # Set default n-gram sizes if none provided
    if ngram_sizes is None:
        ngram_sizes = [1, 2, 3, 4]

    # Map n-gram sizes to their corresponding directory paths
    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    # Print report header
    print("=" * 80)
    print("UNIFIED N-GRAM MATRIX ANALYSIS REPORT")
    print("=" * 80)

    # Dictionary to store all statistics organized by n-gram size
    all_stats = {}

    # Process each requested n-gram size
    for n in ngram_sizes:
        # Validate that we have a path defined for this n-gram size
        if n not in ngram_paths:
            print(f"Warning: No path defined for {n}-gram matrices, skipping...")
            continue

        matrices_path = ngram_paths[n]

        # Check if the directory exists
        if not os.path.exists(matrices_path):
            print(f"Warning: {n}-gram matrices directory not found, skipping...")
            continue

        # Scan directory to find available genre matrices
        available_genres = []
        for filename in os.listdir(matrices_path):
            if filename.startswith("transition_matrix_") and filename.endswith(".npz"):
                # Extract genre name from filename by removing prefix and extension
                genre = filename.replace("transition_matrix_", "").replace(".npz", "")
                available_genres.append(genre)

        # Skip if no matrices found for this n-gram size
        if not available_genres:
            print(f"No {n}-gram matrices found in {matrices_path}")
            continue

        # Print section header for this n-gram size
        print(f"\n{n}-GRAM MATRICES ANALYSIS")
        print("-" * 50)

        # Collect statistics for all genres in this n-gram size
        ngram_stats = []
        for genre in sorted(available_genres):
            # Analyze sparsity for this specific genre and n-gram size
            stats = analyze_matrix_sparsity(genre, n)
            if stats:
                ngram_stats.append(stats)

                # Determine appropriate element type label for display
                element_type = "chords" if n == 1 else f"{n}-grams"

                # Print formatted statistics for this genre
                print(f"{genre:15} | Size: {stats['matrix_shape']} | "
                      f"Density: {stats['density']:.1%} | "
                      f"Active {element_type}: {stats['active_ngrams']}/{stats['total_ngrams']}")

        # Calculate and display summary statistics for this n-gram size
        if ngram_stats:
            # Calculate average density and size across all genres
            avg_density = np.mean([s["density"] for s in ngram_stats])
            avg_size = np.mean([s["total_ngrams"] for s in ngram_stats])
            element_type = "chords" if n == 1 else f"{n}-grams"

            # Print summary line
            print(f"\nSUMMARY: Avg density: {avg_density:.1%}, Avg size: {avg_size:.0f} {element_type}")

            # Store statistics for this n-gram size
            all_stats[n] = ngram_stats

    return all_stats
