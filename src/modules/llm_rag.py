from transformers import pipeline

def search(query, embedder, index, documents, top_k=5):
    query_emb = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, top_k)
    return [documents[i] for i in indices[0]]


def rag_answer(question, embedder, index, documents, model_name="google/flan-t5-base", top_k=5):
    context = "\n".join(search(question, embedder, index, documents, top_k))

    prompt = f"""
Use o contexto abaixo para responder à pergunta.
Se não encontrar nada no contexto, diga que não há informação disponível.

Contexto:
{context}

Pergunta: {question}
Resposta:
"""

    qa_model = pipeline("text2text-generation",
                         model=model_name,
                         do_sample=True,
                         temperature=0.2,
                         early_stopping=True)
    response = qa_model(prompt, max_new_tokens=200)
    return response[0]["generated_text"]
