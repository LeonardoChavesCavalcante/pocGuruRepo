from huggingface_hub import login

def publish_dataset(dataset, repo_id: str):
    # fazer login no Hugging Face
    dataset.push_to_hub(repo_id)
