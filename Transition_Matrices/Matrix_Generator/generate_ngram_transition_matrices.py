import os
import pickle

from datasets import load_dataset

from Transition_Matrices.Matrix_Builder.build_genre_ngram_transition_matrices import \
    build_genre_ngram_transition_matrices
from Utils.path_constants import MATRICES_1_GRAM_PATH, MATRICES_2_GRAM_PATH, MATRICES_3_GRAM_PATH, MATRICES_4_GRAM_PATH


def generate_ngram_transition_matrices(genres_subset=None, ngram_sizes=None, batch_size=5, min_count=2):
    """
    Generates n-gram transition matrices for specified n-gram sizes with filtering support.
    """
    if ngram_sizes is None:
        ngram_sizes = [2, 3, 4]
    try:
        print("Loading dataset...")
        dataset = load_dataset("ailsntua/Chordonomicon")

        print("Extracting genres...")
        main_genres = set(entry["main_genre"] for entry in dataset["train"] if entry["main_genre"])
        main_genres = list(main_genres)

        if genres_subset:
            main_genres = [g for g in main_genres if g in genres_subset]

        print(f"Found {len(main_genres)} genres to process")

        for n in ngram_sizes:
            print(f"\nProcessing {n}-gram matrices...")
            matrices_path = _get_matrices_path(n)
            os.makedirs(matrices_path, exist_ok=True)

            for i in range(0, len(main_genres), batch_size):
                batch_genres = main_genres[i:i + batch_size]
                print(f"Processing batch {i // batch_size + 1}: {batch_genres}")

                # CORRECT - includes min_count parameter
                transition_matrices = build_genre_ngram_transition_matrices(
                    dataset, batch_genres, n, min_count=min_count
                )

                for genre, data in transition_matrices.items():
                    _save_genre_ngram_matrices(genre, data, matrices_path, n)

    except Exception as e:
        print(f"Error generating n-gram transition matrices: {e}")
        raise


def _save_genre_ngram_matrices(genre, data, matrices_path, n):
    """
    Saves the n-gram transition matrix and mappings using unified naming convention.
    Always saves as .npz format for consistency.
    """
    try:
        from scipy.sparse import save_npz, csr_matrix

        # Always save as .npz for consistency
        sparse_file = os.path.join(matrices_path, f"transition_matrix_{genre}.npz")

        if hasattr(data["matrix"], "todense"):
            # Already sparse, save directly
            save_npz(sparse_file, data["matrix"])
        else:
            # Convert dense to sparse and save
            sparse_matrix = csr_matrix(data["matrix"])
            save_npz(sparse_file, sparse_matrix)

        print(f"✓ Saved {genre} {n}-gram matrix (.npz)")

        # Save mappings (unchanged)
        mappings_file = os.path.join(matrices_path, f"ngram_mappings_{genre}.pkl")
        with open(mappings_file, "wb") as f:
            pickle.dump({
                "ngram_to_idx": data["ngram_to_idx"],
                "idx_to_ngram": data["idx_to_ngram"],
                "n": n
            }, f)

        element_type = "chords" if n == 1 else f"{n}-grams"
        matrix_shape = data["matrix"].shape
        total_elements = len(data["ngram_to_idx"])

        print(f"✓ Saved {genre} {n}-gram mappings ({matrix_shape}) - {total_elements} {element_type}")

    except Exception as e:
        print(f"✗ Failed to save {genre} {n}-gram: {e}")


def _get_matrices_path(n):
    """
    Returns the appropriate matrices path for a given n-gram size.
    """
    ngram_paths = {
        1: MATRICES_1_GRAM_PATH,
        2: MATRICES_2_GRAM_PATH,
        3: MATRICES_3_GRAM_PATH,
        4: MATRICES_4_GRAM_PATH
    }

    if n not in ngram_paths:
        raise ValueError(f"Unsupported n-gram size: {n}")

    return ngram_paths[n]