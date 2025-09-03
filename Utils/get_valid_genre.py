from Utils.variable_constants import CHORDONOMICON_GENRES

def get_valid_genre(user_genre: str) -> str:
    """
    Returns the correct genre from CHORDONOMICON_GENRES if user_genre matches (case-insensitive).
    Raises ValueError if not found.
    """
    user_genre_lower = user_genre.strip().lower()

    for genre in CHORDONOMICON_GENRES:
        if genre.lower() == user_genre_lower:
            return genre

    raise ValueError(f"Genre '{user_genre}' not found. Available genres: {', '.join(CHORDONOMICON_GENRES)}")
