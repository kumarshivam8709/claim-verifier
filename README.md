# 🤖 AI-Powered Misinformation Assistant

An end-to-end **Streamlit application** that extracts factual claims from URLs, text, or screenshots, retrieves web evidence, classifies stance, scores risk, and exports a shareable **PDF Credibility Card**.

---

## ✨ Features

- 📌 Extracts clear, verifiable claims from input content using an **LLM fact-checking prompt**.
- 🔎 Retrieves evidence via **SerpAPI Google Search**, compiling snippets, sources, and dates.
- ⚖️ Classifies stance of each evidence item relative to a claim: `SUPPORT`, `REFUTE`, or `NEI` (with confidence & quote span).
- 🧮 Computes a **risk level & score** per claim (`LOW`, `MED`, `HIGH`) using a transparent scoring heuristic.
- 📄 Generates a polished **PDF Credibility Card** with sources and quotes for sharing/archiving.
- 🖼️ Supports input by **URL, raw text, or screenshot**, with optional **Privacy Mode toggle**.

---

## 🏗️ Architecture

1. **Input** – URL fetch via Trafilatura, direct text, or OCR (via OCR.space API).  
2. **Claims** – LLM-based claim extraction → discrete, verifiable statements.  
3. **Retrieval** – SerpAPI GoogleSearch → organic result snippets + metadata.  
4. **Stance** – LLM assigns label, confidence, and justifying quote span.  
5. **Scoring** – Rule-based risk scoring from SUPPORT/REFUTE/NEI distribution.  
6. **Output** – ReportLab-generated PDF Credibility Card.  

---

## 🛠️ Tech Stack

- **UI:** Streamlit  
- **LLM:** OpenAI Chat Completions  
- **Search:** SerpAPI (`google-search-results`)  
- **Parsing:** Trafilatura  
- **OCR:** OCR.space API  
- **PDF:** ReportLab  
- **Utils:** python-dotenv, requests, Pillow, PyTesseract
