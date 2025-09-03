# Guitar Melody Generation with Markov Chains

This project generates guitar melodies using Markov chains, converts chord sequences to MIDI files, and plays them. It supports various genres and instruments.

## Features

- Generate chord sequences for multiple genres
- Convert chord sequences to MIDI files
- Play generated MIDI files
- Easily configurable instrument and genre

## Requirements

- Python 3.13

## Installation

1. Clone the repository:
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script `main.py`:

- `generate_music_sequence`: Generates a music sequence using the specified genre and input parameters.
  - If you provide an input sequence, its length, output length, and genre, the function will:
    - Auto-generate a sequence to match the input length if no sequence is provided.
    - Use the provided chords if the sequence length matches the input length.
    - Generate chords to match the input length based on the input and genre if the sequence length does not match.
  - The available music genres are listed at the top of the `main.py` file.
- `chord_sequence_to_midi`: Converts the generated sequence to a MIDI file.
  - Sample MIDI instruments are listed at the top of the `main.py` file.
- `play_midi`: Plays the specified MIDI file.

## Sources

For this project, the Chordonomicon dataset has been used to analyze the transition probabilities between chords, using the main genres specified as labels in the dataset.

- [Chordonomicon Paper](https://arxiv.org/abs/2410.22046)
- [Chordonomicon Dataset](https://huggingface.co/datasets/ailsntua/Chordonomicon)
