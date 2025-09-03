import os
import json
import uuid
from datetime import datetime
from Utils.path_constants import CHORD_SEQUENCES_PATH

def save_sequence_to_json(input_sequence, generated_sequence):
    """
    Saves input and generated chord sequences to a uniquely named .json file in SEQUENCES_PATH.
    """
    os.makedirs(CHORD_SEQUENCES_PATH, exist_ok=True)
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sequence_{timestamp}_{unique_id}.json"
    filepath = os.path.join(CHORD_SEQUENCES_PATH, filename)

    data = {
        "input_sequence": input_sequence,
        "generated_sequence": generated_sequence
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return filepath