import os
import time
from typing import List, Dict
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

MAX_TEXT_LENGTH = 1_000_000


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []

    for page in reader.pages:
        try:
            txt = page.extract_text()
        except Exception:
            txt = None
        if txt:
            texts.append(txt)

    full_text = "\n".join(texts)

    if full_text.strip():
        return full_text[:MAX_TEXT_LENGTH]

    if OCR_AVAILABLE:
        try:
            images = convert_from_path(path)
            ocr_texts = [pytesseract.image_to_string(img) for img in images]
            return "\n".join(ocr_texts)[:MAX_TEXT_LENGTH]
        except Exception as e:
            print(f"[OCR ERROR] {path}: {e}")
            return ""
    return ""


def process_single_pdf(path: str) -> Dict:
    fname = os.path.basename(path)
    try:
        text = extract_text_from_pdf(path)
        meta = {
            "id": fname,
            "file": path,
            "title": os.path.splitext(fname)[0],
            "size": os.path.getsize(path),
            "modified": time.ctime(os.path.getmtime(path)),
        }
        print(f"[LOADED] {fname} -> {len(text)} chars")
        return {"meta": meta, "text": text}
    except Exception as e:
        print(f"[ERROR] reading {fname}: {e}")
        return None


def load_pdfs_from_folder(folder_path: str) -> List[Dict]:
    """
    Load semua PDF dari folder dan kembalikan list of dict {'id', 'file', 'text'}.
    """
    docs = []
    for fname in os.listdir(folder_path):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(folder_path, fname)
        try:
            reader = PdfReader(path)
            text_pages = []
            for p in reader.pages:
                txt = p.extract_text()
                if txt:
                    text_pages.append(txt)
            full_text = "\n".join(text_pages)
            docs.append({"id": fname, "file": path, "text": full_text})
            print(f"[LOADED] {fname} ({len(text_pages)} pages)")
        except Exception as e:
            print(f"[ERROR] Reading {fname}: {e}")
    return docs