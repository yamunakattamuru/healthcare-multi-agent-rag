from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[1]

CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "healthcare_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def retrieve_documents(query, top_k=4, domain_hint=None):
    """
    Search the healthcare ChromaDB knowledge base
    using semantic similarity.
    """

    if not query or not str(query).strip():
        return []

    try:
        client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        collection = client.get_collection(
            name=COLLECTION_NAME
        )

        model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        query_embedding = model.encode(
            [str(query)],
            convert_to_numpy=True
        )[0].tolist()

        # Search inside the detected healthcare domain
        if domain_hint and domain_hint != "UNKNOWN":

            domain = domain_hint.lower()

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={
                    "domain": domain
                },
                include=[
                    "documents",
                    "metadatas"
                ]
            )

        else:

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas"
                ]
            )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        retrieved = []

        for document, metadata in zip(
            documents,
            metadatas
        ):

            if not document:
                continue

            metadata = metadata or {}

            source = metadata.get(
                "source",
                "unknown.txt"
            )

            domain = metadata.get(
                "domain",
                "unknown"
            )

            filename = metadata.get(
                "filename",
                source
            )

            path = metadata.get(
                "path",
                f"documents/{domain}/{filename}"
            )

            retrieved.append({
                "content": document,
                "source": source,
                "domain": domain,
                "filename": filename,
                "path": path
            })

        return retrieved

    except Exception as error:

        print(
            f"Retrieval error: {error}"
        )

        return []