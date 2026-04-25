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

---

## Prerequisites — External Services

Before running this project, you need accounts and API keys for the following services. None of these are included in the repository — each person setting up the project must create their own.

### Google Gemini
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with a Google account
3. Click **Get API key**
4. Copy the key — this is your `GEMINI_API_KEY`

### Pinecone
1. Go to [pinecone.io](https://www.pinecone.io) and create a free account
2. From the dashboard, go to **API Keys** and copy your key — this is your `PINECONE_API_KEY`
3. The app will auto-create the index on first run with these settings:
   - Index name: `little-angels-rag-index`
   - Dimension: `384`
   - Metric: `cosine`
   - Cloud: `aws`
   - Region: `us-east-1`

### Tavily
1. Go to [tavily.com](https://www.tavily.com) and create a free account
2. From the dashboard, copy your API key — this is your `TAVILI_API_KEY`
3. Note the spelling: `TAVILI` not `TAVILY` — this must match exactly in your `.env` file

### OCR.space
1. Go to [ocr.space](https://ocr.space/ocrapi) and register for a free API key
2. Copy the key — this is your `OCR_API_KEY`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd RAG_Project
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project root with the following contents:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILI_API_KEY=your_tavily_api_key
OCR_API_KEY=your_ocr_space_api_key
```

---

## First-Time Setup — Building The Knowledge Base

These two steps are required the first time you set up the project. They populate the Pinecone index with the school's internal knowledge. Without them, the bot will have no school-specific information to answer from.

### Step 1 — Extract and clean text from school images

Run the image extraction pipeline to process the images in the `images/` folder and generate `cleaned_text.json`:

```bash
python -m rag.image_extraction
```

This uses OCR to extract text from the school images and cleans it using Gemini. The output is saved to `cleaned_text.json`.

### Step 2 — Ingest the school knowledge into Pinecone

Run the ingestion script to embed and store the cleaned text in Pinecone:

```bash
python -m rag.ingest
```

This only needs to be run once. After this, the Pinecone index will contain the school's knowledge and the bot will be able to answer school-related questions.

---

## Running The App

Once the knowledge base is set up, launch the app with:

```bash
python app.py
```

This starts the Gradio-based chatbot interface.

---

## Pinned Versions

This project pins all dependencies to the exact versions it was built and tested against. The key ones are:

- `gradio==5.25.0`
- `langchain==1.2.15`
- `langchain-community==0.4.1`
- `langchain-pinecone==0.2.13`
- `langchain-google-genai==4.2.2`
- `pinecone-client==6.0.0`
- `sentence-transformers==5.4.1`

Do not upgrade any of these without testing for compatibility as breaking changes have been introduced across versions, particularly in Gradio and LangChain.

---

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

---

## Logging

Tool and retrieval activity is logged to:

```text
agent_calls.log
```

This can help debug internal retrieval behavior, web fallback usage, API failures, and upload-related issues.