from rag.retriever import retrieve_documents


def retrieve_context(question, top_k=4, domain_hint=None):
    """
    Retrieve relevant healthcare information for the question.
    """

    results = retrieve_documents(
        question,
        top_k=top_k,
        domain_hint=domain_hint
    )

    if not results:
        return []

    return results