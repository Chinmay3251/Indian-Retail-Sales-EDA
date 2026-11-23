# Setup and Run (Windows PowerShell)

Run each command separately from the extracted project directory.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Optional Ollama mode
1. Install and start Ollama separately.
2. Pull a model, for example:

```powershell
ollama pull qwen2.5:1.5b
```

3. Enable “Use local Ollama LLM” in the app sidebar.

The built-in intent mapping works without Ollama. If the LLM call fails or produces invalid SQL, the app falls back to the built-in mapping.

## Run tests
```powershell
pip install pytest
python -m pytest -q
```
