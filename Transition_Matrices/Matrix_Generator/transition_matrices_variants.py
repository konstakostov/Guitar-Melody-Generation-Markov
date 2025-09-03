from Transition_Matrices.Matrix_Generator.generate_transition_matrices import generate_transition_matrices
from Transition_Matrices.Matrix_Generator.generate_ngram_transition_matrices import generate_ngram_transition_matrices
from Transition_Matrices.Matrix_Analyzer.Sparsity_Analyzer.analyze_all_matrices import analyze_all_matrices


def create_transition_matrices_with_variants(genres_subset=None, include_ngrams=True, ngram_sizes=[2, 3, 4]):
    """
    Create transition matrices using unified n-gram architecture.

    Args:
        genres_subset (list, optional): A list of specific genres to process.
        include_ngrams (bool): Whether to generate n-gram matrices in addition to chord matrices.
        ngram_sizes (list): Which n-gram sizes to generate if include_ngrams is True.
    """
    print("=" * 80)
    print("CREATING UNIFIED N-GRAM MATRICES WITH ANALYSIS")
    print("=" * 80)

    # Step 1: Generate 1-gram (chord) matrices
    print("\nStep 1: Creating 1-gram (chord) transition matrices...")
    generate_transition_matrices(genres_subset=genres_subset)

    # Step 2: Generate higher n-gram matrices
    if include_ngrams and ngram_sizes:
        print(f"\nStep 2: Creating {ngram_sizes}-gram transition matrices...")
        generate_ngram_transition_matrices(genres_subset=genres_subset, ngram_sizes=ngram_sizes)

    # Step 3: Analyze all matrices using unified analyzer
    all_sizes = [1] + (ngram_sizes if include_ngrams else [])
    print(f"\nStep 3: Analyzing all matrices ({all_sizes}-grams)...")
    analyze_all_matrices(ngram_sizes=all_sizes)

    print("\n" + "=" * 80)
    print("UNIFIED MATRICES CREATED AND ANALYZED SUCCESSFULLY")
    print("=" * 80)


def quick_analysis_only(ngram_sizes=None):
    """
    Analyze existing matrices without regenerating using unified approach.

    Args:
        ngram_sizes (list): Which n-gram sizes to analyze.
    """
    if ngram_sizes is None:
        ngram_sizes = [1, 2, 3, 4]

    print("=" * 80)
    print("ANALYZING EXISTING UNIFIED N-GRAM MATRICES")
    print("=" * 80)

    analyze_all_matrices(ngram_sizes=ngram_sizes)

    print("\nANALYSIS COMPLETE")