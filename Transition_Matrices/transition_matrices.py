from Transition_Matrices.Matrix_Generator.generate_transition_matrices import generate_transition_matrices
from Transition_Matrices.Matrix_Generator.transition_matrices_variants import create_transition_matrices_with_variants, \
    quick_analysis_only


def create_transition_matrices():
    """
    Create basic transition matrices (original version).

    This function generates transition matrices for all or a subset of genres
    without performing additional analysis or creating matrix variants.
    """
    generate_transition_matrices()


def create_all_variants():
    """
    Create all matrix variants with analysis.

    This function generates transition matrices for all or a subset of genres,
    performs analysis on the generated matrices, and creates additional matrix variants.
    """
    create_transition_matrices_with_variants()


def analyze_existing_matrices():
    """
    Analyze existing matrices without regenerating.

    This function analyzes the sparsity of existing transition matrices and generates
    a comparison report if optimized matrices are available.
    """
    quick_analysis_only()


if __name__ == "__main__":
    # Choose your approach:

    # Option 1: Basic matrices only
    # create_transition_matrices()

    # Option 2: Full analysis with all variants
    create_all_variants()

    # Option 3: Just analyze existing matrices
    # analyze_existing_matrices()
