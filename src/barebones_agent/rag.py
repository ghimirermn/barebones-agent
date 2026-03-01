import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SUPPORTED_EXTENSIONS = {".txt", ".md", ".py", ".json", ".csv", ".html", ".rst"}

def load_documents(path):
    documents = []
    if os.path.isfile(path):
        documents.append((path, _read(path)))
    else:
        for root, _, files in os.walk(path):
            for fname in files:
                if os.path.splitext(fname)[1].lower() in SUPPORTED_EXTENSIONS:
                    fpath = os.path.join(root, fname)
                    content = _read(fpath)
                    if content:
                        documents.append((fpath, content))
    return documents

def _read(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def chunk_text(text, source, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append({"text": text[start:end], "source": source, "start": start})
        start = end - overlap
    return chunks

def rag_search(query, path, top_k=3):
    docs = load_documents(path)
    all_chunks = []
    for source, content in docs:
        all_chunks.extend(chunk_text(content, source))

    chunk_texts = [c["text"] for c in all_chunks]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(chunk_texts + [query])

    query_vec = tfidf_matrix[-1]
    chunk_vecs = tfidf_matrix[:-1]
    similarities = cosine_similarity(query_vec, chunk_vecs).flatten()
    top_indices = similarities.argsort()[::-1][:top_k]

    results = []
    for rank, idx in enumerate(top_indices, 1):
        chunk = all_chunks[idx]
        score = similarities[idx]
        results.append(f"[{rank}] (score: {score:.3f}) {chunk['source']}\n{chunk['text']}")

    return "\n\n---\n\n".join(results)
