# Project Overview

## Little Angels Montessori RAG Chatbot

An AI-powered school assistant built for Little Angels Montessori using:
- `Gemini` for reasoning and response generation
- `Pinecone` for vector search over internal school knowledge and uploaded files
- `Tavily` for web search fallback
- `Gradio` for the user interface

The chatbot is designed to answer school-related questions from internal knowledge first, while also supporting session-based uploaded documents for retrieval-based Q&A.

## Project Purpose

This project was built as a Retrieval-Augmented Generation (RAG) chatbot for a school setting.

Its main goals are:
- answer questions about Little Angels Montessori from internal documents
- support uploaded files during a user session
- fall back to web search when internal retrieval does not return relevant results
- provide a simple web UI for interacting with the assistant

## Core Features

### School Knowledge Q&A
Answers questions about Little Angels Montessori using internal embedded knowledge stored in Pinecone.

### Uploaded Document Support
Supports session-based uploads for:
- `.pdf`
- `.txt`
- `.png`
- `.jpg`
- `.jpeg`

Uploaded files are processed and added to a session-specific retrieval namespace.

### Web Search Fallback
Uses Tavily search when internal retrieval does not return relevant results for normal queries.

### OCR-Based Image Support
Image uploads are supported through OCR-based text extraction.

This feature is currently experimental and still being improved. At the moment, it is best suited for:
- notices
- posters
- screenshots
- scanned image-based documents

### Gradio Interface
Provides a lightweight chat interface for:
- asking questions
- uploading files
- interacting with the assistant conversationally

## Tech Stack

- `Python`
- `LangChain`
- `Google Gemini`
- `Pinecone`
- `Tavily`
- `Gradio`
- `PyPDF`
- `Sentence Transformers`
- `python-dotenv`
