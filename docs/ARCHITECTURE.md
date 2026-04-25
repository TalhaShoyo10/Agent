# Architecture

## High-Level Flow

1. User submits a message or uploads a file.
2. Uploaded files are extracted and ingested into a session-specific Pinecone namespace.
3. Internal retrieval is attempted first.
4. If relevant internal context is found, Gemini answers from that context.
5. If internal retrieval is empty for a normal query, Tavily web search is used as fallback.
6. Gemini generates the final grounded response.

## Main Components

### `Gemini`
Used for:
- reasoning
- answer generation
- OCR text cleanup support

### `Pinecone`
Used for:
- internal school knowledge retrieval
- session-based uploaded file retrieval
- vector storage and similarity search

### `Tavily`
Used as the external web search fallback when internal retrieval does not produce relevant context.

### `Gradio`
Used to provide the UI for:
- chat interaction
- file uploads
- session-based conversations

### OCR Pipeline
Used for image-based uploads by extracting text before it enters the retrieval pipeline.

## Retrieval Logic

At a high level, the app follows this logic:

1. User submits a message.
2. If uploaded files exist in the session, uploaded/session retrieval is considered.
3. Internal knowledge retrieval is attempted first.
4. If internal retrieval returns useful context, the model answers from that context.
5. If internal retrieval is empty for a normal question, web search can be used as fallback.
6. Gemini generates the final answer.

## Main Files

### `app.py`
Entry point for launching the application.

### `ui/gradio.py`
Contains the Gradio UI and the main session-aware request flow.

### `agent/agent_setup.py`
Configures the LangChain agent and tool setup.

### `agent/tools.py`
Defines:
- internal knowledge search
- web search
- retrieval helpers

### `rag/input_extraction.py`
Extracts content from:
- PDFs
- text files
- image files

### `rag/upload_ingest.py`
Handles:
- session id creation
- upload chunk ingestion into Pinecone
- deletion of session-specific vectors

### `config/configurations.py`
Loads environment variables and initializes:
- Pinecone
- Gemini
- Tavily
- embeddings
