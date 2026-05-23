import gradio as gr
import os
from utils.merger import merge_safetensors

MODELS_DIR = os.path.join(os.getcwd(), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def get_models():
    return sorted([f for f in os.listdir(MODELS_DIR) if f.endswith(".safetensors")])

def run_merge(source_name, target_name, output_filename):
    if not source_name or not target_name:
        return "Error: Please select both source and target models."
    
    if not output_filename:
        output_filename = "merged_model.safetensors"
    
    if not output_filename.endswith(".safetensors"):
        output_filename += ".safetensors"

    source_path = os.path.join(MODELS_DIR, source_name)
    target_path = os.path.join(MODELS_DIR, target_name)
    output_path = os.path.join(MODELS_DIR, output_filename)

    success, message = merge_safetensors(source_path, target_path, output_path)
    
    if success:
        return f"✅ Success!\n\n{message}"
    else:
        return f"❌ Failed!\n\n{message}"

def refresh_models():
    models = get_models()
    return gr.Dropdown(choices=models), gr.Dropdown(choices=models)

# UI Definition
with gr.Blocks(title="Safetensors Key Merger") as demo:
    gr.Markdown("# Safetensors Key Merger")
    gr.Markdown("Extracts `vae.`, `audio_vae.`, `vocoder.`, and `text_embedding_projection.` from Source and overwrites/adds them to Target.")
    gr.Markdown(f"Place your `.safetensors` files in: `{MODELS_DIR}`")
    
    with gr.Row():
        with gr.Column():
            model_list = get_models()
            source_input = gr.Dropdown(label="Source Safetensor (The donor)", choices=model_list)
            target_input = gr.Dropdown(label="Target Safetensor (The recipient)", choices=model_list)
            refresh_btn = gr.Button("🔄 Refresh Model List")
            
            output_name = gr.Textbox(label="Output Filename", placeholder="merged_model.safetensors", value="merged_model.safetensors")
            merge_btn = gr.Button("Start Merge", variant="primary")
        
        with gr.Column():
            status_output = gr.Textbox(label="Process Status", interactive=False, lines=10)

    merge_btn.click(
        fn=run_merge,
        inputs=[source_input, target_input, output_name],
        outputs=status_output
    )
    
    refresh_btn.click(
        fn=refresh_models,
        inputs=[],
        outputs=[source_input, target_input]
    )

if __name__ == "__main__":
    demo.launch()
