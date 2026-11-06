"""
RAG retrieval and generation:
Question -> SentenceTransformer embedding -> FAISS retrieval
-> retrieved context -> Ollama Llama 3.2 -> grounded answer.
"""

from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from ollama import chat

ROOT = Path(__file__).resolve().parent
VECTORSTORE_DIR = ROOT / "vectorstore"
INDEX_PATH = VECTORSTORE_DIR / "faiss.index"
METADATA_PATH = VECTORSTORE_DIR / "metadata.json"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2:1b"
TOP_K = 4


class RAGPipeline:
    def __init__(self):
        if not INDEX_PATH.exists() or not METADATA_PATH.exists():
            raise FileNotFoundError(
                "FAISS index not found. Upload PDF files and build the knowledge base first."
            )

        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.index = faiss.read_index(str(INDEX_PATH))
        self.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

        if self.index.ntotal != len(self.metadata):
            raise ValueError("FAISS index and metadata count do not match. Rebuild the index.")

    def retrieve(self, question: str, top_k=TOP_K):
        query_vector = self.embedding_model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vector, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            item = dict(self.metadata[int(idx)])
            item["score"] = float(score)
            results.append(item)
        return results

    def answer(self, question: str, top_k=TOP_K):
        question = question.strip()
        if not question:
            raise ValueError("Please enter a question.")

        retrieved = self.retrieve(question, top_k=top_k)
        if not retrieved:
            return "Information not available in the uploaded documents.", []

        context_parts = []
        for item in retrieved:
            context_parts.append(
                f"[Source: {item['source']}, page: {item['page']}]\n{item['text']}"
            )
        context = "\n\n".join(context_parts)

        prompt = f"""You are an assistant that answers questions about uploaded documents.

Use ONLY the information in the context below.
If the answer is not supported by the context, say:
"Information not available in the uploaded documents."
Do not invent facts. When useful, mention the source filename and page number.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

        response = chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.message.content, retrieved
