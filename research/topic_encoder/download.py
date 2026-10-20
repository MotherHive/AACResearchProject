from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Alibaba-NLP/gte-modernbert-base",
    revision="e7f32e3c00f91d699e8c43b53106206bcc72bb22",
    local_dir="base_model",
    allow_patterns=["*.json", "*.safetensors", "*.txt", "README.md"],
)