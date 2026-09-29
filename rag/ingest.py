from pathlib import Path
import hashlib
import chromadb
from sentence_transformers import SentenceTransformer
from rag.create_documents import create_documents


BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "healthcare_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100):
    """Split a document into overlapping chunks."""

    cleaned = text.strip()

    if not cleaned:
        return []

    if len(cleaned) <= chunk_size:
        return [cleaned]

    chunks = []
    start = 0

    while start < len(cleaned):
        end = start + chunk_size
        chunk = cleaned[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(cleaned):
            break

        start += chunk_size - overlap

    return chunks


def ingest_documents():
    """Store healthcare documents in ChromaDB."""

    create_documents()

    if not DOCS_DIR.exists():
        print(f"Documents directory not found: {DOCS_DIR}")
        return 0

    text_files = sorted(DOCS_DIR.rglob("*.txt"))

    print(f"Discovered {len(text_files)} documents.")

    if not text_files:
        print("No .txt files were found.")
        return 0

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    existing_ids = set(
        collection.get(include=[]).get("ids", [])
    )

    model = SentenceTransformer(EMBEDDING_MODEL)

    all_chunks = []

    for file_path in text_files:

        relative_path = file_path.relative_to(BASE_DIR).as_posix()

        domain = (
            file_path.parent.name
            if file_path.parent != DOCS_DIR
            else "unknown"
        )

        try:
            text = file_path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Skipping {relative_path}: {exc}")
            continue

        for index, chunk in enumerate(
            split_text_into_chunks(text)
        ):

            file_hash = hashlib.sha256(
                relative_path.encode("utf-8")
            ).hexdigest()[:16]

            chunk_id = f"{file_hash}_{index}"

            if chunk_id in existing_ids:
                continue

            all_chunks.append({
                "id": chunk_id,
                "content": chunk,
                "source": file_path.name,
                "domain": domain,
                "filename": file_path.name,
                "path": relative_path
            })

            existing_ids.add(chunk_id)

    if not all_chunks:
        print("No new chunks to index.")
        return 0

    embeddings = model.encode(
        [item["content"] for item in all_chunks],
        convert_to_numpy=True
    )

    collection.add(
        embeddings=list(embeddings),
        documents=[
            item["content"]
            for item in all_chunks
        ],
        metadatas=[
            {
                "source": item["source"],
                "domain": item["domain"],
                "filename": item["filename"],
                "path": item["path"]
            }
            for item in all_chunks
        ],
        ids=[
            item["id"]
            for item in all_chunks
        ]
    )

    print(
        f"Indexed {len(all_chunks)} chunks into ChromaDB."
    )

    return len(all_chunks)


if __name__ == "__main__":
    ingest_documents()