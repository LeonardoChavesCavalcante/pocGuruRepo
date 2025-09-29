from modules.prepare_dataset import prepare_dataset
from modules.publish_dataset import publish_dataset
from modules.embeddings_index import build_index
from modules.llm_rag import rag_answer

def main():
    # 1) Preparar dataset
    dataset = prepare_dataset("data/jabref_github_data.json")

    # 2) Publicar no Hugging Face Hub (opcional)
    # publish_dataset(dataset, "seu-usuario/jabref-github-data")

    # 3) Criar embeddings + índice
    embedder, index, documents = build_index(dataset)

    # 4) Perguntar para a LLM com RAG
    perguntas = [
        "Quais issues o usuário koppor abriu em agosto de 2025?",
        "Quem são os colaboradores com permissão de admin?",
        "Quais commits foram feitos em agosto de 2025?"
    ]


    for pergunta in perguntas:
        resposta = rag_answer(pergunta, embedder, index, documents)
        print(f"========================================================")        
        print(f"{pergunta}?")
        print(f"")        
        print(f"{resposta}")
        print(f"========================================================")

if __name__ == "__main__":
    main()
