from typing import List, Dict
from utils.embed import VectorStore

def retrieve_context(query: str, top_k: int = 3) -> List[Dict]:
    """
    Mengambil konteks relevan dari vector store untuk pertanyaan pengguna.
    """
    vs = VectorStore()
    try:
        results = vs.retrieve(query, top_k=top_k)
        return results
    except Exception as e:
        print(f"[RETRIEVE ERROR] {e}")
        return []