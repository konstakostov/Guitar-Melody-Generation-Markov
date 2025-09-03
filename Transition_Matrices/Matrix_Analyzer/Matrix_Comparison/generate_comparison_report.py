import os
import numpy as np

from Transition_Matrices.Matrix_Analyzer.Matrix_Comparison.compare_matrix_versions import compare_matrix_versions, \
    compare_all_adjacent_ngrams
from Utils.path_constants import MATRICES_1_GRAM_PATH, MATRICES_2_GRAM_PATH, MATRICES_3_GRAM_PATH, MATRICES_4_GRAM_PATH


def generate_comparison_report(ngram_sizes=None):
    """
    Generate a unified comparison report for transition matrices across multiple n-gram sizes.

    This function scans directories for each n-gram size, identifies genres that have matrices
    for multiple n-gram sizes, and compares adjacent n-gram matrices (e.g., 1-gram vs 2-gram,
    2-gram vs 3-gram) for each genre. It provides detailed analysis of how matrix properties
    change as n-gram order increases.

    Args:
        ngram_sizes (list of int, optional): List of n-gram sizes to include in the comparison.
            Must be values from [1, 2, 3, 4]. Defaults to [1, 2, 3, 4].

    Returns:
        dict: Dictionary mapping each comparable genre (str) to its list of comparison results.
            Each comparison result is a dict containing:
            - 'n1', 'n2': The two n-gram sizes being compared
            - 'size_change': Percentage change in matrix size
            - 'density_change': Percentage change in matrix density
            - 'element_type1', 'element_type2': Type of elements in each matrix
            - 'elements1_count', 'elements2_count': Number of elements in each matrix
    """
    if ngram_sizes is None:
        ngram_sizes = [1, 2, 3, 4]

    # Map n-gram sizes to their corresponding directory paths
    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    # Track which n-gram sizes are available for each genre
    genre_availability = {}

    # Scan each n-gram directory to find available genres
    for n in ngram_sizes:
        if n not in ngram_paths or not os.path.exists(ngram_paths[n]):
            continue

        for filename in os.listdir(ngram_paths[n]):
            if filename.startswith("transition_matrix_") and filename.endswith(".npz"):
                # Extract genre name from filename
                genre = filename.replace("transition_matrix_", "").replace(".npz", "")
                if genre not in genre_availability:
                    genre_availability[genre] = []
                genre_availability[genre].append(n)

    # Filter to only genres with multiple n-gram sizes available
    comparable_genres = {g: sizes for g, sizes in genre_availability.items() if len(sizes) > 1}

    if not comparable_genres:
        print("No genres found with multiple n-gram sizes for comparison")
        return {}

    # Print report header
    print("=" * 80)
    print("UNIFIED N-GRAM MATRIX COMPARISON REPORT")
    print("=" * 80)

    all_comparisons = {}

    # Generate comparisons for each genre
    for genre in sorted(comparable_genres.keys()):
        print(f"\n🎵 {genre.upper()}")
        print("-" * 40)

        # Compare all adjacent n-gram pairs for this genre
        genre_comparisons = compare_all_adjacent_ngrams(genre)

        if genre_comparisons:
            all_comparisons[genre] = genre_comparisons

            # Print detailed comparison results for this genre
            for comparison in genre_comparisons:
                n1, n2 = comparison['n1'], comparison['n2']
                size_change = comparison['size_change']
                density_change = comparison['density_change']

                print(f"{n1}-gram vs {n2}-gram:")
                print(f"    Size change: {size_change:+.1%}")
                print(f"    Density change: {density_change:+.1%}")
                print(f"    {comparison['element_type1']}: {comparison['elements1_count']} → "
                      f"    {comparison['element_type2']}: {comparison['elements2_count']}")

    # Generate and print summary statistics
    if all_comparisons:
        print(f"\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)

        # Collect all size and density changes across all comparisons
        all_size_changes = []
        all_density_changes = []

        for genre_comps in all_comparisons.values():
            for comp in genre_comps:
                all_size_changes.append(comp["size_change"])
                all_density_changes.append(comp["density_change"])

        if all_size_changes:
            avg_size_change = np.mean(all_size_changes)
            avg_density_change = np.mean(all_density_changes)

            print(f"Average size change: {avg_size_change:+.1%}")
            print(f"Average density change: {avg_density_change:+.1%}")
            print(f"Total genres analyzed: {len(all_comparisons)}")
            print(f"Total comparisons: {len(all_size_changes)}")

    return all_comparisons


def generate_specific_comparison_report(n1=1, n2=2):
    """
    Generate a comparison report between two specific n-gram sizes for all available genres.

    This function finds genres that have transition matrices for both specified n-gram sizes,
    performs direct comparisons between them, and provides a detailed analysis of the
    differences in matrix properties.

    Args:
        n1 (int, optional): The first n-gram size to compare. Must be in [1, 2, 3, 4].
            Defaults to 1.
        n2 (int, optional): The second n-gram size to compare. Must be in [1, 2, 3, 4].
            Defaults to 2.

    Returns:
        list: List of comparison result dictionaries, one for each genre where both
            n-gram sizes are available. Each dictionary contains:
            - 'genre': Name of the genre
            - 'n1', 'n2': The two n-gram sizes being compared
            - 'size1', 'size2': Matrix sizes for each n-gram
            - 'density1', 'density2': Matrix densities for each n-gram
            - 'size_change': Percentage change in matrix size
            - 'density_change': Percentage change in matrix density
            - 'element_type1', 'element_type2': Type of elements in each matrix
            - 'elements1_count', 'elements2_count': Number of elements in each matrix
    """
    # Map n-gram sizes to their corresponding directory paths
    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    # Validate input n-gram sizes
    if n1 not in ngram_paths or n2 not in ngram_paths:
        print(f"Error: Unsupported n-gram sizes {n1} or {n2}")
        return []

    # Find genres available for each n-gram size
    genres1 = set()
    genres2 = set()

    # Scan directory for first n-gram size
    if os.path.exists(ngram_paths[n1]):
        for f in os.listdir(ngram_paths[n1]):
            if f.startswith("transition_matrix_") and f.endswith(".npy"):
                # Extract genre name from filename
                genre = f.replace("transition_matrix_", "").replace(".npz", "")
                genres1.add(genre)

    # Scan directory for second n-gram size
    if os.path.exists(ngram_paths[n2]):
        for f in os.listdir(ngram_paths[n2]):
            if f.startswith("transition_matrix_") and f.endswith(".npz"):
                # Extract genre name from filename
                genre = f.replace("transition_matrix_", "").replace(".npz", "")
                genres2.add(genre)

    # Find genres that have matrices for both n-gram sizes
    common_genres = genres1.intersection(genres2)

    if not common_genres:
        print(f"No common genres found between {n1}-gram and {n2}-gram matrices")
        return []

    # Print report header
    print(f"=" * 80)
    print(f"{n1}-GRAM vs {n2}-GRAM COMPARISON REPORT")
    print("=" * 80)

    comparisons = []

    # Generate comparison for each common genre
    for genre in sorted(common_genres):
        comparison = compare_matrix_versions(genre, n1, n2)
        if comparison:
            comparisons.append(comparison)

            # Print detailed results for this genre
            print(f"\n{genre.upper()}")
            print(f"Size: {comparison['size1']} → {comparison['size2']} ({comparison['size_change']:+.1%})")
            print(f"Density: {comparison['density1']:.1%} → {comparison['density2']:.1%} ({comparison['density_change']:+.1%})")
            print(f"{comparison['element_type1']}: {comparison['elements1_count']} → "
                  f"{comparison['element_type2']}: {comparison['elements2_count']}")

    # Generate and print summary statistics
    if comparisons:
        print(f"\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        # Calculate average changes across all genres
        avg_size_change = np.mean([c['size_change'] for c in comparisons])
        avg_density_change = np.mean([c['density_change'] for c in comparisons])

        print(f"Average size change: {avg_size_change:+.1%}")
        print(f"Average density change: {avg_density_change:+.1%}")
        print(f"Genres compared: {len(comparisons)}")

    return comparisons
