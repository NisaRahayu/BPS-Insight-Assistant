import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

class VectorStore:
    def __init__(self, index_path="vector_store/index.faiss", meta_path="vector_store/meta.json"):
        self.index_path = index_path
        self.meta_path = meta_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.meta = []

        os.makedirs(os.path.dirname(index_path), exist_ok=True)

    def build(self, docs):
        texts = [doc["text"] for doc in docs]
        embeddings = self.model.encode(texts, convert_to_numpy=True).astype("float32")

        # Buat index FAISS
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.meta = docs
        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
            print("Vector store loaded successfully.")
        else:
            print("Vector store belum dibuat. Jalankan upload PDF dulu.")

    def retrieve(self, query, top_k=3):
        if self.index is None:
            self.load()

        if self.index is None:
            raise ValueError("Index FAISS belum tersedia. Jalankan upload dokumen terlebih dahulu.")

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(self.meta):
                continue
            results.append(self.meta[idx])
        return results
