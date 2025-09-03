import os


# The absolute path to the project directory.
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Path to the "Audio_Input" directory within the project.
AUDIO_INPUT_PATH = os.path.join(ROOT_PATH, "Audio_Input")

# Path to the "Data" directory within the project.
DATA_PATH = os.path.join(ROOT_PATH, "Data")

# Path to the "Chord_Sequences" directory inside the "Data" directory.
CHORD_SEQUENCES_PATH = os.path.join(DATA_PATH, "Chord_Sequences")

# Path to the "Chroma_Chords" directory inside the "Data" directory.
CHROMA_CHORDS_PATH = os.path.join(DATA_PATH, "Chroma_Chords")

# Path to the "Matrices" directory within the project.
MATRICES_PATH = os.path.join(DATA_PATH, "Matrices")

# Path to the "Matrices_1_Gram" directory inside the "Matrices" directory.
MATRICES_1_GRAM_PATH = os.path.join(MATRICES_PATH, "Matrices_1_Gram")

# Path to the "Matrices_1_Gram" directory inside the "Matrices" directory.
MATRICES_2_GRAM_PATH = os.path.join(MATRICES_PATH, "Matrices_2_Gram")

# Path to the "Matrices_1_Gram" directory inside the "Matrices" directory.
MATRICES_3_GRAM_PATH = os.path.join(MATRICES_PATH, "Matrices_3_Gram")

# Path to the "Matrices_1_Gram" directory inside the "Matrices" directory.
MATRICES_4_GRAM_PATH = os.path.join(MATRICES_PATH, "Matrices_4_Gram")

# Path to the "Midi_Sequences" directory inside the "Data" directory.
MIDI_SEQUENCES_PATH = os.path.join(DATA_PATH, "Midi_Sequences")

# Path to the "Markov_Chains" directory within the project.
MARKOV_CHAINS_PATH = os.path.join(ROOT_PATH, "Markov_Chains")

# Path to the "Transition_Matrices" directory within the project.
TRANSITION_MATRICES_PATH = os.path.join(ROOT_PATH, "Transition_Matrices")

# Path to the "Data_Processor" directory inside the "TRANSITION_MATRICES_PATH" directory.
DATA_PROCESSOR_PATH = os.path.join(TRANSITION_MATRICES_PATH, "Data_Processor")

# Path to the "Matrix_Analyzer" directory inside the "TRANSITION_MATRICES_PATH" directory.
MATRIX_ANALYZER_PATH = os.path.join(TRANSITION_MATRICES_PATH, "Matrix_Analyzer")

# Path to the "Matrix_Comparison" directory inside the "Matrix_Analyzer" directory.
MATRIX_COMPARISON_PATH = os.path.join(MATRIX_ANALYZER_PATH, "Matrix_Comparison")

# Path to the "Sparsity_Analyzer" directory inside the "Matrix_Analyzer" directory.
SPARSITY_ANALYZER_PATH = os.path.join(MATRIX_ANALYZER_PATH, "Sparsity_Analyzer")

# Path to the "Matrix_Builder" directory inside the "TRANSITION_MATRICES_PATH" directory.
MATRIX_BUILDER_PATH = os.path.join(TRANSITION_MATRICES_PATH, "Matrix_Builder")

# Path to the "Matrix_Optimizer" directory inside the "TRANSITION_MATRICES_PATH" directory.
MATRIX_OPTIMIZER_PATH = os.path.join(TRANSITION_MATRICES_PATH, "Matrix_Optimizer")

# Path to the "Utils" directory within the project.
UTILS_PATH = os.path.join(ROOT_PATH, "Utils")

# Path to the "Chroma_Chords" directory inside the "Utils" directory.
CHROMA_CHORDS_GENERATION_PATH = os.path.join(UTILS_PATH, "Chroma_Chords")

# Path to the "Midi_Utils" directory inside the "Utils" directory.
MIDI_UTILS_PATH = os.path.join(ROOT_PATH, "Midi_Utils")
