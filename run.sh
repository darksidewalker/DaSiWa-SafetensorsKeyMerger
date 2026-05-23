#!/bin/bash
set -e

# --- 1. CONFIGURATION ---
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_DIR/.venv"

echo "📂 Project Root: $PROJECT_DIR"

# --- 2. SYSTEM DEPENDENCIES ---
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "🔍 Detected System: $NAME"

    case "$ID" in
        arch|manjaro)
            echo "📦 Checking build tools for Arch-based system..."
            sudo pacman -S --needed --noconfirm base-devel cmake curl
            ;;
        ubuntu|debian|mint)
            echo "📦 Checking build tools for Debian-based system..."
            sudo apt update
            sudo apt install -y build-essential cmake curl
            ;;
        *)
            echo "⚠️ Unrecognized distribution ($ID). Ensure build-essential, cmake, and curl are installed."
            ;;
    esac

    # Install 'uv' if missing
    if ! command -v uv &> /dev/null; then
        echo "⚙️ uv not found. Installing via official script..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
    else
        echo "✅ uv is already installed."
    fi
else
    echo "❌ Could not detect OS via /etc/os-release. Skipping system package install."
fi

# --- 3. LOCAL VENV SETUP ---
cd "$PROJECT_DIR"

if [ ! -d "$VENV_PATH" ]; then
    echo "⚙️ Creating local virtual environment..."
    uv venv "$VENV_PATH"
fi

echo "📦 Syncing Python dependencies..."
uv pip install -r requirements.txt

# --- 4. LAUNCH ---
echo "🚀 Starting Safetensors Merger..."

# Activate environment and run
export VIRTUAL_ENV="$VENV_PATH"
export PATH="$VENV_PATH/bin:$PATH"

python app.py
