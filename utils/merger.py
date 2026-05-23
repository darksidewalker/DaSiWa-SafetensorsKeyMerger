import torch
from safetensors.torch import load_file, save_file
from safetensors import safe_open
import os

# The specific prefixes requested
TARGET_PREFIXES = [
    "vae.",
    "audio_vae.",
    "vocoder.",
    "text_embedding_projection."
]

def merge_safetensors(source_path, target_path, output_path):
    """
    Extracts specific keys from source and overwrites/adds them to target.
    """
    if not os.path.exists(source_path):
        return False, f"Source file not found: {source_path}"
    if not os.path.exists(target_path):
        return False, f"Target file not found: {target_path}"

    try:
        # Load target dictionary fully to keep all other layers intact
        target_dict = load_file(target_path)
        
        # Open source and target for metadata and selective extraction
        source_dict = {}
        source_metadata = None
        target_metadata = None

        with safe_open(source_path, framework="pt", device="cpu") as f:
            source_metadata = f.metadata()
            for key in f.keys():
                if any(key.startswith(p) for p in TARGET_PREFIXES):
                    source_dict[key] = f.get_tensor(key)

        with safe_open(target_path, framework="pt", device="cpu") as f:
            target_metadata = f.metadata()

        merged_count = 0
        for key, tensor in source_dict.items():
            target_dict[key] = tensor
            merged_count += 1

        # Merge metadata (Source metadata adds/overwrites Target metadata)
        final_metadata = (target_metadata or {}).copy()
        if source_metadata:
            final_metadata.update(source_metadata)
        
        # Save the result
        save_file(target_dict, output_path, metadata=final_metadata if final_metadata else None)
        
        return True, f"Successfully transferred {merged_count} keys.\nSaved to: {output_path}"
    
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
