def verify_answer(answer, context, analysis=None):
    """Check the answer before showing it to the user."""

    if not answer or not answer.strip():
        return "No answer was generated. Please try another question."

    if context and context[0].get("source") == "no_source_available.txt":
        return (
            "I could not find enough relevant educational information "
            "in the local healthcare knowledge base. "
            "Please ask a question related to the provided healthcare documents."
        )

    domain = (analysis or {}).get("domain", "UNKNOWN")

    return (
        f"{answer}\n\n"
        f"Note: This is synthetic educational content for a hackathon "
        f"demonstration in the {domain} domain and does not replace "
        f"professional medical advice or diagnosis."
    )