# Setup And Usage

## Project Structure

```text
RAG_Project/
│
├── agent/
│   ├── agent_setup.py
│   ├── llm.py
│   └── tools.py
│
├── config/
│   └── configurations.py
│
├── rag/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── get_namespace.py
│   ├── image_extraction.py
│   ├── ingest.py
│   ├── input_extraction.py
│   └── upload_ingest.py
│
├── ui/
│   └── gradio.py
│
├── graphics/
│   └── logo.png
│
├── images/
│   └── internal source images
│
├── app.py
├── requirements.txt
├── school_theme.css
├── cleaned_text.json
├── CHANGELOG.md
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd RAG_Project
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILI_API_KEY=your_tavily_api_key
OCR_API_KEY=your_ocr_api_key
```

### Variable Usage

- `GEMINI_API_KEY`: main reasoning model and OCR cleanup support
- `PINECONE_API_KEY`: vector index and retrieval
- `TAVILI_API_KEY`: web search fallback
- `OCR_API_KEY`: image text extraction

## Running The App

Launch the app with:

```bash
python -m app
```

or:

```bash
python app.py
```

This starts the Gradio-based chatbot interface.

## Configuration Notes

### Pinecone Index

The project auto-creates the Pinecone index if it does not already exist.

Current configuration:
- Index name: `little-angels-rag-index`
- Dimension: `384`
- Metric: `cosine`
- Cloud: `aws`
- Region: `us-east-1`

### Gemini Models

Current model setup:
- `gemini-3-flash-preview` for main reasoning
- `gemini-2.5-flash-lite` for OCR text cleaning

## Example Queries

### School Questions

- `What are the school timings?`
- `What are the monthly fees?`
- `Tell me about the summer camp.`
- `What programs does the school offer?`

### Uploaded Document Questions

Best results come from specific content-bearing prompts:
- `What does the uploaded document say about leadership?`
- `What does the uploaded PDF say about empathy?`
- `Does the uploaded article mention emotional intelligence?`

### Image-Based Questions

Currently experimental:
- `What text is written in this uploaded notice?`
- `What does this poster say?`
- `Does this image mention school timings?`

## Logging

Tool and retrieval activity is logged to:

```text
agent_calls.log
```

This can help debug:
- internal retrieval behavior
- web fallback usage
- API failures
- upload-related issues

## Testing / Helper Files

The repository includes utility and test files such as:
- `gemini_test.py`
- `tavili_test.py`
- `test_agent.py`
- `test_retrieval.py`
