from Audio_Input.chord_sequence_controller import ChordSequenceController
from Markov_Chains.markov_chain_sequence_generator import MarkovChainSequenceGenerator
from Markov_Chains.ngram_matrix_loader import NGramMatrixLoader
from Utils.get_valid_genre import get_valid_genre
from Utils.save_sequence_to_json import save_sequence_to_json


def generate_music_sequence(in_seq, in_len, out_len, m_genre):
    """
    Generate a musical chord sequence using genre-specific Markov chain models.

    This function orchestrates the complete music generation workflow: validates and
    processes input parameters, prepares the initial chord sequence, loads the appropriate
    genre-specific transition matrices, generates new chord sequences using Markov chain
    analysis, and saves the results to JSON format for further processing or analysis.

    Args:
        in_seq (list or str): Initial chord sequence to seed the generation process.
            Can be a list of chord symbols ['C', 'Am', 'F'] or a string representation.
            This sequence provides the starting context for Markov chain generation.
        in_len (int): Desired length of the processed input sequence. If the provided
            in_seq is shorter, it may be extended; if longer, it may be truncated.
            Must be a positive integer representing the number of chords.
        out_len (int): Length of the output sequence to generate. Must be a positive
            integer representing the number of new chords to generate beyond the input.
        m_genre (str): Musical genre for the Markov model. Examples: 'blues', 'jazz',
            'rock', 'pop'. Case-insensitive. Must correspond to available trained models.

    Returns:
        None: The function prints results and saves output to JSON files, but does not
            return a value. Generated sequences are saved to the Data/Chord_Sequences/
            directory with timestamped filenames.

    Raises:
        ValueError: If the genre is invalid or not supported by the available models.
        SystemExit: If critical validation errors occur that prevent execution.
    """
    # Store the initial input sequence for processing
    initial_sequence = in_seq
    input_sequence = None  # Will be populated by the controller

    # Store sequence length parameters for clarity
    input_sequence_length = in_len
    output_sequence_length = out_len

    # Normalize genre name to lowercase for consistent lookup
    genre = m_genre.lower()

    # Validate that the specified genre is supported by the system
    try:
        genre = get_valid_genre(genre)
    except ValueError as e:
        print("Error:", e)
        exit(1)  # Exit if genre validation fails

    # Initialize the chord sequence controller with input parameters
    controller = ChordSequenceController(initial_sequence, input_sequence_length, genre)

    # Process the initial sequence to create a properly formatted input sequence
    try:
        input_sequence = controller.get_sequence()
        print("Initial chord sequence:", input_sequence)
    except ValueError as e:
        print("Error:", e)
        # Continue execution even if sequence processing has issues

    # Load the pre-trained n-gram transition matrices for the specified genre
    ngram_loader = NGramMatrixLoader(genre=genre)  # Initialize with required parameters

    # Create the Markov chain generator with the loaded matrices
    markov_generator = MarkovChainSequenceGenerator(ngram_loader)

    # Generate the new chord sequence using Markov chain probability analysis
    output_sequence = markov_generator.generate_sequence(input_sequence, output_sequence_length)

    print("Markov chain generated chord sequence:", output_sequence)

    # Save both input and output sequences to JSON format for analysis or playback
    filepath = save_sequence_to_json(input_sequence, output_sequence)
    print(f"Input and Output Sequences Saved to: {filepath}")
