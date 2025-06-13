from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import base64
import io
import pytesseract

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# === FastAPI app ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load vector DB ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local(
    "vector_store",
    embeddings=embedding,
    allow_dangerous_deserialization=True
)

class Query(BaseModel):
    question: str
    image: Optional[str] = None

@app.get("/")
def root():
    return {"message": "✅ TDS Virtual TA API is live!"}

@app.post("/")
async def ask_query(query: Query):
    question_text = query.question.strip()

    if query.image:
        try:
            image_bytes = base64.b64decode(query.image)
            image = Image.open(io.BytesIO(image_bytes))
            extracted_text = pytesseract.image_to_string(image)
            question_text += "\n" + extracted_text
        except Exception as e:
            print("⚠️ OCR error:", e)

    results = db.similarity_search(question_text, k=4)

    if not results:
        return {
            "answer": "Sorry, I couldn't find anything relevant.",
            "links": []
        }

    answer_text = "\n\n".join([r.page_content for r in results[:4]])

    return {
        "answer": answer_text,
        "links": [
            {
                "url": r.metadata.get("source", "#"),
                "text": r.page_content[:150].replace("\n", " ") + "..."
            }
            for r in results
        ]
    }
