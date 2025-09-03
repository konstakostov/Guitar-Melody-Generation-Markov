import pygame


def play_midi(midi_file_path):
    """
    Play a MIDI file using pygame's audio mixer.

    This function initializes pygame's audio system, loads and plays the specified
    MIDI file, waits for playback to complete, then cleans up pygame resources.
    The function blocks until the entire MIDI file has finished playing.

    Args:
        midi_file_path (str): Absolute or relative path to the MIDI file to play.
            The file must be a valid MIDI format (.mid or .midi) that pygame
            can handle. Path should be accessible from the current working directory.

    Returns:
        None: The function performs playback and does not return a value.

    Raises:
        pygame.error: If pygame fails to initialize or load the MIDI file.
        FileNotFoundError: If the specified MIDI file path does not exist.
        OSError: If there are audio system issues or permission problems.
    """
    # Initialize pygame and its audio mixer subsystem
    pygame.init()
    pygame.mixer.init()

    # Load the MIDI file into pygame's music system
    pygame.mixer.music.load(midi_file_path)

    # Start playback of the loaded MIDI file
    pygame.mixer.music.play()

    # Wait for the MIDI file to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(20)

    # Clean up pygame resources after playback completes
    pygame.quit()
