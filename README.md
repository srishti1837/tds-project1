# 🧠 TDS Virtual TA API

A virtual assistant that answers student queries using **IITM’s Tools in Data Science (TDS)** course material and **Discourse forum** discussions.

---

## ⚠️ Disclaimer

> **Use this data at your own risk.**  
> While every effort has been made to accurately scrape and structure the data, no guarantee is made about its completeness or correctness.

---

## 📦 Contents

This repository includes:
- `discourse_posts.json`: All posts from the Discourse TDS KB forum (Jan 1 – Jun 14, 2025).
- `discourse_json/`: Individual topic-wise post streams from the Discourse forum.
- `tds_pages_md/`: Scraped Markdown content from [TDS 2025-01](https://tds.s-anand.net/#/2025-01/).
- `vector_store/index.pkl`: FAISS vector index built on embedded content.
- `app.py`: FastAPI app exposing a `/ask` endpoint for question answering.
- `embedder.py`: Script to embed scraped content using OpenAI or Gemini.
- `scraper/`: Scrapers used to collect website and Discourse data.

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Srishti2313/Project1-tds.git

```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the API Server
```bash
uvicorn app:app --reload
````
## 🧪 API Usage
### Endpoint
bash
```
POST /ask
```
### Request Format
json
```
{
  "question": "Explain bias-variance tradeoff.",
  "image": "<optional base64 image string>"
}
```
### Response Format
json
```
{
  "answer": "The bias-variance tradeoff refers to ...",
  "links": [
    "https://discourse.onlinedegree.iitm.ac.in/t/ga5-overfitting",
    "https://tds.s-anand.net/#/2025-01/ml/bias-variance"
  ]
}
```
