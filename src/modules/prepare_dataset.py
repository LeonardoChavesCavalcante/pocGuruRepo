from datasets import Dataset
import json
import os

def prepare_dataset(json_path: str, cache_path: str = "dataset_cache"):
    
    # Se o dataset já foi salvo antes, carrega direto
    if os.path.exists(cache_path):
        print(f"Carregando dataset do cache: {cache_path}")
        return Dataset.load_from_disk(cache_path)

    # Senão, cria o dataset a partir do JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []

    for issue in data.get("issues", []):
        records.append({
            "type": "issue",
            "id": issue.get("number"),
            "title": issue.get("title"),
            "author": issue.get("author", {}).get("login"),
            "createdAt": issue.get("createdAt")
        })

    for pr in data.get("pullRequests", []):
        records.append({
            "type": "pull_request",
            "id": pr.get("number"),
            "title": pr.get("title"),
            "author": pr.get("author", {}).get("login"),
            "createdAt": pr.get("createdAt"),
            "state": pr.get("state")
        })

    for commit in data.get("commits", []):
        records.append({
            "type": "commit",
            "id": commit.get("oid"),
            "title": commit.get("message"),
            "author": commit.get("author", {}).get("user", {}).get("login"),
            "createdAt": commit.get("committedDate")
        })

    for collab in data.get("collaborators", []):
        records.append({
            "type": "collaborator",
            "id": collab.get("login"),
            "title": "Collaborator",
            "author": collab.get("login"),
            "createdAt": collab.get("addedAt"),
            "permission": collab.get("permission")
        })

    dataset = Dataset.from_list(records)

    # Salva para reutilização futura
    dataset.save_to_disk(cache_path)
    print(f"Dataset salvo em: {cache_path}")

    return dataset
