# Deployment Guide

## Overview

This guide explains how to:
- upload the project to GitHub without Git installed
- host the project on Hugging Face Spaces
- avoid uploading local-only or sensitive files

This project can be deployed using only the browser, so Git is not required.

---

## Before You Upload

Make sure you do **not** upload the following:
- `.env`
- `venv/`
- `__pycache__/`
- `.gradio/`
- `agent_calls.log`

These files are either:
- local-only
- generated files
- environment-specific
- or contain secrets

---

## Files And Folders To Upload

Upload these project files and folders:

- `agent/`
- `config/`
- `docs/`
- `graphics/`
- `images/`
- `rag/`
- `ui/`
- `app.py`
- `requirements.txt`
- `README.md`
- `CHANGELOG.md`
- `school_theme.css`

Upload `cleaned_text.json` only if your production app still depends on it.

---

## Part 1: Upload To GitHub Without Git

### Step 1: Create a GitHub repository

1. Go to `https://github.com`
2. Sign in
3. Click `New repository`
4. Enter your repository name
5. Choose public or private
6. Do **not** initialize it with a README if your local project already has one
7. Click `Create repository`

### Step 2: Upload files through the browser

1. Open the new repository
2. Click `Add file`
3. Click `Upload files`
4. Drag and drop your project files and folders
5. Add a commit message such as:

```text
Initial project upload
```

6. Click `Commit changes`

---

## Part 2: Host On Hugging Face Spaces

### Step 1: Create a Space

1. Go to `https://huggingface.co`
2. Sign in
3. Click `New Space`
4. Enter a Space name
5. Choose `Gradio` as the SDK
6. Choose public or private
7. Create the Space

### Step 2: Upload your project files

Once the Space is created:

1. Open the Space
2. Use the file upload interface in the browser
3. Upload the same project files and folders listed earlier

Do **not** upload:
- `.env`
- `venv/`
- `__pycache__/`
- `.gradio/`
- `agent_calls.log`

---

## Hugging Face Secrets

After uploading the files:

1. Open your Space
2. Go to `Settings`
3. Open the `Variables and secrets` section
4. Add the required secrets

Add these exact names:

```text
GEMINI_API_KEY
PINECONE_API_KEY
TAVILI_API_KEY
OCR_API_KEY
```

Important:
- your code currently uses `TAVILI_API_KEY`
- so the Hugging Face secret must use that exact spelling unless you rename it in code

---

## App Launch Notes

Your app is already structured around Gradio, so Hugging Face should run it as long as:
- `app.py` exists at the project root
- `requirements.txt` exists at the project root
- your Gradio app launches correctly

For Hugging Face Spaces:
- `share=True` is not needed
- `css_paths=...` is fine if it works with your current Gradio version

If your current launch line looks like this:

```python
demo.queue().launch(share=True, css_paths=css_path)
```

then the safer Hugging Face version is:

```python
demo.queue().launch(css_paths=css_path)
```

---

## Suggested `.gitignore`

If you later install Git, this is a good starting `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environment
venv/
.venv/

# Environment / secrets
.env

# Logs
*.log
agent_calls.log

# Gradio / local app state
.gradio/

# OS / editor
.DS_Store
Thumbs.db
.vscode/
.idea/

# Test / cache
.pytest_cache/
.mypy_cache/
```

---

## Deployment Checklist

Before deployment:
- confirm `.env` is not uploaded
- confirm `venv/` is not uploaded
- confirm `requirements.txt` is present
- confirm `app.py` is present at the root
- confirm `school_theme.css` is present if your app references it
- confirm all required folders are uploaded
- confirm Hugging Face secrets are added

After deployment:
- open the Hugging Face Space
- wait for the build to finish
- test a normal school query
- test an uploaded document query
- test whether CSS loads correctly

---

## Recommended Workflow For Now

Since Git is not installed yet, the simplest workflow is:

1. Upload the project to GitHub using the browser
2. Upload the project to Hugging Face Spaces using the browser
3. Add secrets manually in Hugging Face
4. Test the deployed app

Later, if you want a smoother workflow, you can install:
- Git for Windows
- GitHub Desktop
- or use built-in source control from VS Code

---

## Final Note

This project is deployable without Git, but browser upload works best when you are selective about what you include.

Keep secrets out of uploaded files, and rely on Hugging Face Space secrets for API keys.
