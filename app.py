import os
import streamlit as st
from dotenv import load_dotenv
from utils.embed import VectorStore
from utils.retriever import retrieve_context
from utils.pdf_loader import load_pdfs_from_folder

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

try:
    from google import genai
    from google.genai import Client
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False

st.set_page_config(page_title="📊 BPS Insight Assistant", layout="wide")
st.title("📊 BPS Insight Assistant")
st.caption("Asisten interaktif untuk menjelajahi publikasi resmi BPS.")

# ====================================
# Sidebar
# ====================================
with st.sidebar:
    st.header("📁 Manajemen Dokumen")
    st.write("Unggah publikasi BPS yang ingin digunakan untuk menjawab pertanyaan.")
    upload = st.file_uploader("Unggah file PDF", type=["pdf"], accept_multiple_files=True)
    upload_btn = st.button("📤 Simpan & Proses Dokumen")
    
    st.markdown("---")
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.success("Chat berhasil direset!")

# ====================================
# Inisialisasi Gemini otomatis
# ====================================
if GENAI_AVAILABLE and "genai_client" not in st.session_state:
    try:
        st.session_state.genai_client = Client()
    except Exception as e:
        st.sidebar.error(f"Gagal menginisialisasi Gemini: {e}")

# ====================================
# Proses upload dokumen
# ====================================
if upload_btn and upload:
    os.makedirs("data", exist_ok=True)
    for f in upload:
        path = os.path.join("data", f.name)
        with open(path, "wb") as out:
            out.write(f.getbuffer())
        st.success(f"📄 {f.name} berhasil disimpan.")

    st.info("Membangun index vektor, harap tunggu...")
    vs = VectorStore()
    docs = load_pdfs_from_folder("data")
    vs.build(docs)
    st.success("Dokumen berhasil diproses dan siap digunakan.")

# ====================================
# Inisialisasi memory percakapan
# ====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan percakapan sebelumnya
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ====================================
# Chat input
# ====================================
prompt = st.chat_input("Ketik pertanyaan tentang publikasi BPS...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    contexts = []
    try:
        vs = VectorStore()
        vs.load()
        contexts = vs.retrieve(prompt, top_k=3)
    except Exception as e:
        st.warning(f"⚠️ Basis data dokumen belum siap: {e}")

    if contexts:
        context_text = "\n\n".join([f"Sumber: {c['file']}\n{c['text']}" for c in contexts])
    else:
        context_text = "Tidak ada konteks ditemukan."

    system_prompt = f"""
Anda adalah BPS Insight BOT, asisten virtual resmi dari Badan Pusat Statistik (BPS). 
Gunakan informasi yang tersedia dari dokumen resmi BPS, publikasi, serta file yang diunggah oleh pengguna untuk memberikan jawaban.

Petunjuk untuk menjawab:
1. Jawablah pertanyaan pengguna dengan informasi yang **akurat, jelas, dan terpercaya**.
2. Jawaban harus **singkat, profesional, dan dalam bahasa Indonesia**.
3. Jika informasi tidak tersedia di dokumen atau sumber yang diberikan, katakan dengan jujur bahwa data tersebut tidak tersedia.
4. Sertakan referensi atau sumber dari dokumen BPS atau file yang diunggah jika memungkinkan.
5. Fokus pada fakta, hindari opini atau spekulasi yang tidak berdasar.

KONTEKS:
{context_text}

PERTANYAAN:
{prompt}
"""
    answer = ""
    if GENAI_AVAILABLE:
        try:
            chat = st.session_state.genai_client.chats.create(model=GEMINI_MODEL)
            resp = chat.send_message(system_prompt)
            answer = getattr(resp, "text", str(resp))
        except Exception as e:
            answer = f"[GEMINI ERROR] {e}\n\nBerikut konteks terkait:\n{context_text}"
    else:
        if contexts:
            snippets = "\n\n".join([c["text"][:800] + ("..." if len(c["text"]) > 800 else "") for c in contexts])
            answer = f"Ringkasan dokumen terkait:\n\n{snippets}"
        else:
            answer = "Belum ada dokumen yang dapat digunakan sebagai referensi."

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
