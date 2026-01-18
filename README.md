**RAG-Based Document Assistant**
==============================
<p align="center">
  <img src="https://img.shields.io/badge/Model-OpenAI_GPT--4-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-teal?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Container-Docker-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Library-LangChain-orange?style=for-the-badge" />
</p>

A **production-ready RAG (Retrieval-Augmented Generation) Chatbot** that allows users to **chat with their PDF documents**. Built with **FastAPI**, **LangChain**, and **Docker**, it features a clear, **premium glassmorphic UI** and provides **precise source citations** for every answer.

Designed as a **scalable template** for building internal knowledge bases, document analysis tools, and AI assistants.

---

## 🚀 **Features**

- **Context-Aware Answers**: Uses **RAG** to answer questions specifically based on your uploaded document.

- **Production-Ready Backend**:
  - Built with **FastAPI** for high performance and async support.
  - Fully **Dockerized** for easy deployment.

- **Premium UI Experience**:
  - minimalist **Glassmorphic** design.
  - Smooth **micro-animations** (fade-ins, typing indicators).
  - Integrated **pill-shaped chat bar** with file upload.

- **Transparent AI**:
  - innovative **Source Citations** showing exactly which part of the document was used.
  - Clear **status indicators** for indexing and processing.

- **No Database Required**: Uses in-memory FAISS vector store for simplicity (easily extensible to Pinecone/Weaviate).

---

## 🧰 **Tech Stack**
| Component | Used For |
|----------|----------|
| **Python 3.9+** | Core application logic |
| **FastAPI** | High-performance REST API |
| **LangChain** | RAG framework & document chain |
| **OpenAI API** | LLM (GPT-4/3.5) & Embeddings |
| **FAISS** | Vector store for similarity search |
| **Docker** | Containerization & Deployment |
| **Vanilla JS/CSS** | Lightweight, custom frontend |

---

## 📂 **Project Structure**

```
rag-chatbot/
│── .env (set your OpenAI API Key here)
│── .dockerignore
│── Dockerfile
│── main.py            # FastAPI entry point
│── rag_engine.py      # Core RAG logic (LangChain/FAISS)
│── requirements.txt
│── static/            # CSS, JS, and Assets
│   ├── style.css
│   └── script.js
│── templates/         # HTML Templates
    └── index.html
```

---

## 🖥️ **How It Works**

### **1️⃣ Upload Document**
✔ User uploads a PDF via the UI  
✔ The app uses `PyPDFLoader` to extract text  
✔ Text is split into chunks using `RecursiveCharacterTextSplitter`

---

### **2️⃣ Indexing (Embeddings)**
The app:
- Generates embeddings using **OpenAIEmbeddings**
- Stores them in a local **FAISS** vector index for fast retrieval

---

### **3️⃣ Retrieval & Generation**
- User asks a question
- System retrieves the **top k relevant chunks** from the vector store
- LLM generates an answer using retrieved context + prompt

---

### **4️⃣ Response with Citations**
- The answer is streamed back to the UI
- Used source chunks are displayed below the message for verification

---

## ▶️ **Run Locally**

### **Option 1: Docker (Recommended)**

**Build the Image**
```bash
docker build -t rag-app .
```

**Run the Container**
```bash
docker run -p 8000:8000 --env-file .env rag-app
```

Then visit: [http://localhost:8000](http://localhost:8000)

---

### **Option 2: Python Direct**

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Launch the Server**
```bash
uvicorn main:app --reload
```

Then visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔑 **Setup OpenAI API Key**
</br>

>[!IMPORTANT]
>You must set your OpenAI API Key to use the generation and embedding features.

</br>

Create a `.env` file in the project root:

### **.env File**
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

---

## ⭐ **Future Improvements**

* Multi-document support (chat with a whole folder)
* Persistent vector database (Pinecone/ChromaDB)
* Chat history memory (Session-based)
* Support for Word/Excel/Notion sources
* User Authentication

---

## 🤝 **Contributing**

Pull requests are welcome!
If you want to extend this into a **SaaS product** or add new features, feel free to fork and contribute.

---

## 📄 **License**

MIT
