# 📌 AKA Studio Design Chatbot — Local LLM Only

This project is a **Client Requirement Collection Chatbot** for AKA Studio.
It works fully offline with your own **TinyLlama local LLM**.

---

## 🚀 What’s Inside?

✅ **Flask backend** (`app.py`): Matches client input to your design dataset, generates a friendly suggestion using your own LLM.  
✅ **FastAPI wrapper** (`main.py`): Wraps your TinyLlama running in Ollama.  
✅ **Frontend pages**: `index.html`, `chat.html`, `summary.html`, `thankyou.html`.  
✅ **Dataset**: `aka_studio_designs.xlsx`.

---

## ✅ 1️⃣ Requirements

- Python 3.9+
- pip
- ~3GB RAM
- [Ollama installed](https://ollama.com/download)

---

## ✅ 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ✅ 3️⃣ Pull TinyLlama

```bash
ollama pull tinyllama
```

---

## ✅ 4️⃣ Run TinyLlama

```bash
ollama run tinyllama
```

---

## ✅ 5️⃣ Start FastAPI wrapper

```bash
uvicorn main:app --reload --port 8000
```

---

## ✅ 6️⃣ Run Flask server

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

✅ **No Gemini needed — fully offline, local LLM-powered!**
