# LexAssist — Troubleshooting Guide for Student Developers

This guide explains common errors you may encounter and the exact steps to fix them.

---

## 1. PowerShell Script Execution Policy Error
**Error Message:**
```text
File ... Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```
**Why it happens:**
Windows PowerShell by default restricts running scripts downloaded or created on the computer to prevent accidental malware execution.

**How to fix it:**
Run PowerShell as Administrator, or in your current VS Code terminal run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
Then run the activation command again:
```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 2. Gemini API Key Missing or Invalid
**Error Message:**
```text
ValueError: GEMINI_API_KEY environment variable is not set.
```
**Why it happens:**
The program looks for your key in a file named `.env`, but either the file does not exist, or the key is empty.

**How to fix it:**
1. Check that you copied `.env.example` to `.env` in the project root:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and replace `your_gemini_api_key_here` with your actual key from [Google AI Studio](https://aistudio.google.com/).
3. Make sure there are no spaces around the `=` sign.

---

## 3. ChromaDB SQLite Version Error
**Error Message:**
```text
RuntimeError: Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.
```
**Why it happens:**
Older Python versions or bare environments on certain operating systems have an outdated SQLite binary.

**How to fix it:**
We use Python 3.11.9 on Windows, which bundles SQLite 3.45+. Ensure you are using the virtual environment created with `py -3.11`:
```powershell
.\.venv\Scripts\python.exe -c "import sqlite3; print(sqlite3.sqlite_version)"
```
It should print a version >= 3.35.0.

---

## 4. Port 8501 Already in Use (Streamlit)
**Error Message:**
```text
Port 8501 is already in use
```
**Why it happens:**
A previous Streamlit session was not stopped before running a new one.

**How to fix it:**
Either stop the running session in your terminal (press `Ctrl + C`), or specify a new port:
```powershell
streamlit run app.py --server.port 8502
```
