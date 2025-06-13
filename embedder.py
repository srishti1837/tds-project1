import os
import json
import re
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# === Embedding setup ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
documents = []

# === Load Discourse posts ===
if os.path.exists("discourse_posts.json"):
    with open("discourse_posts.json", "r", encoding="utf-8") as f:
        discourse_posts = json.load(f)

    for post in discourse_posts:
        title = post.get("topic_title", "").strip()
        content = post.get("content", "").strip()
        if not title and not content:
            continue
        full_text = f"{title}\n{content}"
        documents.append(Document(
            page_content=full_text,
            metadata={"source": post.get("url", "")}
        ))
    print(f"✅ Loaded {len(discourse_posts)} Discourse posts.")
else:
    print("⚠️ 'discourse_posts.json' not found.")

# === Load course markdown pages ===
md_dir = "tds_pages_md"
md_file_count = 0

if os.path.exists(md_dir):
    for filename in os.listdir(md_dir):
        if filename.endswith(".md"):
            md_file_count += 1
            path = os.path.join(md_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.search(r'original_url:\s*"(.*?)"', content)
            url = match.group(1) if match else filename

            documents.append(Document(
                page_content=content,
                metadata={"source": url}
            ))
    print(f"✅ Loaded {md_file_count} markdown files from '{md_dir}'.")
else:
    print("⚠️ 'tds_pages_md/' not found.")

# === Save vector DB ===
print(f"🔄 Embedding {len(documents)} documents...")
db = FAISS.from_documents(documents, embedding)
db.save_local("vector_store")
print("✅ Vector store saved to 'vector_store/'")
