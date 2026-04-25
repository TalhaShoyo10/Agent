# Limitations And Future Work

## Current Strengths

The system currently works best for:
- school-specific retrieval-based Q&A
- targeted questions over uploaded files
- internal-first, web-fallback question answering
- session-based retrieval over temporary uploaded content

## Current Limitations

### Uploaded Document Summarization
The current architecture is not yet optimized for full document summarization.

Prompts such as:
- `summarize the uploaded document`
- `tell me about this PDF`
- `what is in this file`

may not work reliably yet, because the uploaded document flow is still retrieval-oriented rather than summary-oriented.

### Experimental Image Feature
Image support currently relies on OCR-based text extraction, not full visual reasoning.

This means performance may vary depending on:
- image quality
- text clarity
- layout complexity
- OCR accuracy

### Session State
Uploaded file awareness currently depends on runtime session state and is not yet fully durable across restarts.

## Future Improvements

Planned next steps include:
- direct uploaded-document summarization
- better handling of vague file-based prompts
- stronger session persistence
- improved OCR quality
- better support for posters, scanned notices, and school image documents
- more reliable image-based retrieval
- clearer separation between:
  - school assistant mode
  - uploaded document assistant mode
  - future summarization mode

## Recommended Usage Right Now

Best-supported use cases:
- school-related factual Q&A
- uploaded document Q&A with specific topic-bearing questions
- internal-first retrieval with web fallback for normal queries

Less-supported use cases:
- whole-document summarization
- vague uploaded-file prompts
- deep multi-document reasoning
