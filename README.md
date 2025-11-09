# 📊 BPS Insight Assistant

**BPS Insight Assistant** adalah chatbot berbasis **RAG (Retrieval-Augmented Generation)** yang dirancang untuk membantu pengguna memperoleh informasi terkait **data dan statistik resmi dari Badan Pusat Statistik (BPS)**.  
Chatbot ini menggabungkan kemampuan **retrieval** dari dokumen (misalnya PDF atau teks internal) dengan **Large Language Model (LLM)** untuk memberikan jawaban yang **relevan, kontekstual, dan akurat**.


## 🚀 Fitur Utama
- 🧠 **RAG-Based Chatbot**: Menggunakan kombinasi *retrieval* dan *generation* untuk menjawab pertanyaan berbasis dokumen.
- 📄 **Integrasi PDF**: Dapat membaca dan mengekstrak informasi dari dokumen BPS (misal: publikasi, laporan, metadata).
- 💬 **Antarmuka Chat Interaktif**: Dibangun menggunakan **Streamlit** agar mudah digunakan secara lokal maupun daring.
- ⚙️ **Dukungan Open Source Model**: Dapat dikonfigurasi menggunakan model LLM lokal atau API (misalnya OpenAI, Ollama, atau HuggingFace).


## 🧩 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/NisaRahayu/BPS-Insight-Assistant.git
cd BPS-Insight-Assistant
```

### 2. Menggunakan venv atau conda agar lingkungan kerja terisolasi.
```bash
python -m venv rag-env
source rag-env/bin/activate      # untuk Linux/Mac
rag-env\Scripts\activate         # untuk Windows
```

### 3. Buat file .env dengan menyalin contoh berikut:
```bash
cp .env.example .env
```

### 4. Isi variabel penting sesuai konfigurasi Anda:
```bash
GOOGLE_API_KEY=your_API_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### 5. Instal Dependensi dan ingest
```bash
pip install -r requirements.txt
python ingest.py
```

### 6. Jalankan Chatbot
```bash
streamlit run app.py
```