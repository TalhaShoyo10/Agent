# Little Angels Montessori AI Assistant

An AI-powered school assistant built with Retrieval-Augmented Generation (RAG). It answers questions about Little Angels Montessori from internal school knowledge, supports session-based document uploads for Q&A, and falls back to live web search when needed.

---

## Demo

> Hosted on Hugging Face Spaces — [link coming soon]

---

## Features

- **School Knowledge Q&A** — answers questions about fees, timings, admissions, and summer camp from embedded internal documents
- **Uploaded Document Support** — upload PDFs, text files, or images during a session and ask questions about them
- **Web Search Fallback** — uses Tavily search when internal retrieval finds nothing relevant
- **OCR-Based Image Support** — extracts and cleans text from uploaded images and scanned notices *(experimental)*
- **Session Management** — each user gets an isolated retrieval namespace that is cleaned up after inactivity

---

## Tech Stack

| Component | Purpose |
|---|---|
| Google Gemini | Reasoning, response generation, OCR cleanup |
| Pinecone | Vector storage and similarity search |
| Tavily | Web search fallback |
| LangChain | Agent and tool orchestration |
| Sentence Transformers | Embedding model (`all-MiniLM-L6-v2`) |
| Gradio | Chat UI and file upload interface |
| OCR.space | Image text extraction |

---

## Project Structure

```
RAG_Project/
├── agent/
│   ├── agent_setup.py       # LangChain agent configuration
│   ├── llm.py               # Gemini model setup
│   └── tools.py             # Internal search and web search tools
├── config/
│   └── configurations.py    # Environment loading, client initialization
├── rag/
│   ├── chunker.py           # Text chunking for ingestion
│   ├── embeddings.py        # Embedding model loader
│   ├── get_namespace.py     # Pinecone namespace helper
│   ├── image_extraction.py  # Offline image OCR pipeline
│   ├── ingest.py            # Ingest cleaned_text.json into Pinecone
│   ├── input_extraction.py  # Extract content from uploaded files
│   └── upload_ingest.py     # Session-based upload ingestion
├── ui/
│   └── gradio.py            # Gradio UI and chat logic
├── docs/                    # Detailed documentation
├── graphics/                # Logo and UI assets
├── images/                  # Internal source images for school knowledge
├── app.py                   # Entry point
├── requirements.txt
└── school_theme.css
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILI_API_KEY=your_tavily_api_key
OCR_API_KEY=your_ocr_space_api_key
```

### 5. Run the app

```bash
python app.py
```

---

## Example Queries

**School questions**
- `What are the school timings?`
- `What are the monthly fees?`
- `Tell me about the summer camp.`

**Uploaded document questions** *(upload a file first, then ask)*
- `What does the uploaded document say about leadership?`
- `Summarize the uploaded PDF.`

---

## Documentation

Detailed documentation is available in the [`docs/`](docs/) folder, covering architecture, setup and usage, deployment, and known limitations and future work.

---

## Deployment

This project is deployed on Hugging Face Spaces. See the [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) for full step-by-step instructions including how to add API keys as Hugging Face secrets.

---

## Notes

- The Pinecone index is auto-created on first run if it does not already exist
- Uploaded file vectors are scoped to the user session and deleted after 10 minutes of inactivity
- Image OCR support is experimental and works best with clearly printed text