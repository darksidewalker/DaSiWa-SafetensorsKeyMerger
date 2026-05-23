# LTX23 Safetensors Merger

A specialized tool designed to extract and merge specific components from `.safetensors` files. It is particularly useful for transferring VAEs, Audio VAEs, Vocoders, and Text Embedding Projections between models.

## Features
- **Selective Merging**: Only transfers specific keys (`vae.`, `audio_vae.`, `vocoder.`, `text_embedding_projection.`).
- **Metadata Preservation**: Merges metadata from both source and target files, ensuring model information is kept intact.
- **Easy Setup**: Automated environment configuration using `uv` for high-performance dependency management.
- **User Friendly**: Simple Gradio-based web interface for easy model selection and processing.

## Installation & Setup

### Prerequisites
- Linux (Ubuntu/Debian or Arch-based recommended).
- Python 3.8+

### Quick Start
1. Clone the repository.
2. Place your `.safetensors` models in the `models/` directory (created automatically on first run).
3. Run the launch script:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

The script will automatically handle system dependencies (like `build-essential` and `cmake`), install the `uv` package manager if missing, create a virtual environment, and launch the web UI.

## Usage
1. Open the Gradio link provided in the terminal (usually `http://127.0.0.1:7860`).
2. **Source Safetensor**: Select the "donor" model that contains the VAE or Vocoder you want to extract.
3. **Target Safetensor**: Select the "recipient" model you want to inject the components into.
4. **Output Filename**: Provide a name for the new merged file.
5. Click **Start Merge**.

## Project Structure
- `app.py`: The Gradio web interface and UI logic.
- `utils/merger.py`: Core logic for selective key extraction and tensor merging.
- `run.sh`: Automated setup, dependency management, and launch script.
- `models/`: The default directory for model storage.

## License
MIT
