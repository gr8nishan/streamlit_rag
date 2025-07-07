# 🔍 Streamlit RAG: Retrieval‑Augmented Generation App

A **Streamlit-based application** for querying documents using Retrieval‑Augmented Generation (RAG). This tool enables users to upload their own documents (PDFs, text files), and ask questions against them using the power of LLMs and vector embeddings.

---

## ✨ Features

- 📄 **Document Upload & Chunking**  
  Upload one or more PDF/Text files. The documents are split into meaningful chunks for embedding and retrieval.

- 🧠 **Embedding & Vector Store**  
  Converts chunks into vector embeddings and stores them in a local vector database (e.g., FAISS or Chroma).

- 💬 **RAG-Powered Chat Interface**  
  Uses retrieved document context + LLM to answer user queries with high accuracy.

- ⚙️ **Configurable Backend**  
  Choose between OpenAI or open-source LLMs and customize chunk size, embedding model, and more.

- 🖥️ **Streamlit UI**  
  Intuitive interface for uploading files, configuring parameters, and chatting in real-time.

---

## 🚀 How It Works

1. **Upload**: Drag and drop your documents into the UI.
2. **Process**: The app splits them into chunks, embeds them, and saves them in a vector store.
3. **Ask**: Submit a question via the chat. The app retrieves relevant chunks and passes them along with your query to the LLM.
4. **Respond**: Get an informed answer based on your documents.

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss) or [Chroma](https://www.trychroma.com/)
- [OpenAI API](https://platform.openai.com/) or [HuggingFace Transformers](https://huggingface.co/transformers/)
- PDF/Text parsing libraries

---


## 📦 Setup Instructions

```bash
git clone https://github.com/gr8nishan/streamlit_rag.git
cd streamlit_rag
pip install -r requirements.txt
streamlit run app.py
