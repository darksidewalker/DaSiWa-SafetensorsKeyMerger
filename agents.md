# Agent Documentation

## Project Overview
This project is a Python-based utility for manipulating `.safetensors` files. It performs "surgery" on model weights, specifically replacing or adding specific component keys from a source model into a target model without altering the remaining architecture.

## Core Logic: `utils/merger.py`
The merging process uses `torch` and the `safetensors` library for memory-efficient tensor manipulation.

- **Target Prefixes**: The extraction is filtered by the following prefixes:
  - `vae.`
  - `audio_vae.`
  - `vocoder.`
  - `text_embedding_projection.`

- **Process Flow**:
  1. **Full Load**: The target model is loaded into memory to serve as the base.
  2. **Selective Extraction**: The source model is opened using `safe_open` to extract only the tensors matching the target prefixes, minimizing memory overhead.
  3. **Injection**: Source tensors overwrite existing keys or add new keys to the target dictionary.
  4. **Metadata Merge**: Metadata from the source is merged into the target metadata (source takes precedence).
  5. **Serialization**: The resulting dictionary and metadata are saved to the specified output path.

## Technical Stack
- **Framework**: PyTorch (`torch`)
- **Format**: `safetensors` (for safety and speed)
- **Interface**: `gradio`
- **Environment**: `uv` (Fast Python package installer and resolver)

## Directory Map
- `/app.py`: Handles model discovery and UI state.
- `/utils/merger.py`: Functional core of the weight merging logic.
- `/run.sh`: Entry point for environment bootstrap and execution.