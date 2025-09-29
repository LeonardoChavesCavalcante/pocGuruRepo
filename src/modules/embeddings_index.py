from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def build_index(dataset):
    documents = []
    for item in dataset:
        text = f"{item['type'].capitalize()} {item['id']} - {item['title']} (Autor: {item['author']}, Criado em {item['createdAt']})"
        if item['type'] == "collaborator":
            text += f" [Permissão: {item.get('permission')}]"
        documents.append(text)

    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embedder.encode(documents, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return embedder, index, documents
