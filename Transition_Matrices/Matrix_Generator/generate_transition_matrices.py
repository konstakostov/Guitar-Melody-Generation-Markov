import os
import pickle
from datasets import load_dataset

from Transition_Matrices.Matrix_Builder.build_genre_transition_matrices import build_genre_transition_matrices
from Utils.path_constants import MATRICES_1_GRAM_PATH


def generate_transition_matrices(genres_subset=None, batch_size=5):
    """
    Generates transition matrices for a subset of genres from a dataset.

    This function loads a dataset of songs, extracts the main genres, and processes them
    in batches to build transition matrices for each genre. The matrices and their chord
    mappings are saved to the specified path.

    Args:
        genres_subset (list, optional): A list of genres to process. If None, all genres
                                        in the dataset are processed. Defaults to None.
        batch_size (int, optional): The number of genres to process in each batch.
                                    Defaults to 10.

    Raises:
        Exception: If an error occurs during dataset loading, matrix generation, or saving.
    """
    try:
        print("Loading dataset...")
        dataset = load_dataset("ailsntua/Chordonomicon")

        print("Extracting genres...")
        main_genres = set(entry["main_genre"] for entry in dataset["train"] if entry[""'main_genre'])
        main_genres = list(main_genres)

        if genres_subset:
            main_genres = [g for g in main_genres if g in genres_subset]

        print(f"Found {len(main_genres)} genres to process")

        os.makedirs(MATRICES_1_GRAM_PATH, exist_ok=True)

        for i in range(0, len(main_genres), batch_size):
            batch_genres = main_genres[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1}: {batch_genres}")

            transition_matrices = build_genre_transition_matrices(dataset, batch_genres)

            for genre, data in transition_matrices.items():
                _save_genre_matrices(genre, data)

        print(f"All matrices saved to: {MATRICES_1_GRAM_PATH}")

    except Exception as e:
        print(f"Error generating transition matrices: {e}")
        raise


def _save_genre_matrices(genre, data):
    """
    Saves the transition matrix and mappings using unified naming convention.
    Always saves as .npz format for consistency.
    """
    try:
        from scipy.sparse import save_npz, csr_matrix

        # Always save as .npz for consistency
        sparse_file = os.path.join(MATRICES_1_GRAM_PATH, f"transition_matrix_{genre}.npz")

        if hasattr(data["matrix"], "todense"):
            save_npz(sparse_file, data["matrix"])
        else:
            sparse_matrix = csr_matrix(data["matrix"])
            save_npz(sparse_file, sparse_matrix)

        # Save mappings (unchanged)
        mappings_file = os.path.join(MATRICES_1_GRAM_PATH, f"ngram_mappings_{genre}.pkl")
        with open(mappings_file, "wb") as f:
            pickle.dump({
                "ngram_to_idx": data["chord_to_idx"],
                "idx_to_ngram": data["idx_to_chord"],
                "n": 1
            }, f)

        print(f"✓ Saved {genre} 1-gram matrix ({data["matrix"].shape}) - {len(data["chord_to_idx"])} chords")

    except Exception as e:
        print(f"✗ Failed to save {genre}: {e}")