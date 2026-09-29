from core.llm import call_llm


def explain_answer(question, context, analysis=None):
    """Generate a detailed healthcare educational explanation."""

    if not context:
        return (
            "No relevant healthcare information was found "
            "in the knowledge base."
        )

    topic = (analysis or {}).get(
        "topic",
        "General Health"
    )

    domain = (analysis or {}).get(
        "domain",
        "UNKNOWN"
    )

    context_text = "\n\n".join(
        f"Source: {item.get('source', 'Unknown')}\n"
        f"Domain: {item.get('domain', 'Unknown')}\n"
        f"Content:\n{item.get('content', '')}"
        for item in context
    )

    system_prompt = f"""
You are the Explanation Agent in a healthcare
multi-agent RAG system.

The user's topic is:
{topic}

The healthcare domain is:
{domain}

Your job is to create a detailed, clear,
easy-to-understand educational explanation
using ONLY the retrieved healthcare information.

Organize the response with these sections
when the retrieved information supports them:

# {topic}

## 1. Definition
Explain what the condition or topic means.

## 2. Common Symptoms
Describe the symptoms mentioned in the
retrieved healthcare information.

## 3. Causes or Triggers
Explain the causes or triggers supported
by the retrieved information.

## 4. Risk Factors
Include relevant risk factors if available.

## 5. Evaluation
Explain how the condition may be evaluated
according to the retrieved information.

## 6. Treatment / Management
Explain only the general management or
treatment concepts supported by the documents.

Do NOT provide:
- Personal diagnosis
- Medicine prescriptions
- Medication dosages
- Personalized treatment plans

## 7. Prevention
Explain prevention or healthy practices
supported by the documents.

## 8. When to Seek Medical Help
Mention warning signs or situations requiring
professional medical evaluation if supported
by the documents.

## Important Note
Explain that this is synthetic educational
content created for a hackathon demonstration
and does not replace professional medical advice.

IMPORTANT:
- Use ONLY the retrieved context.
- Do not invent information.
- If a section is not supported by the retrieved
  documents, say that the available knowledge
  base does not provide enough information.
- Keep the language simple and educational.
- Give a detailed answer, not a short summary.
"""

    user_prompt = f"""
User Question:
{question}

Retrieved Healthcare Information:
{context_text}

Create the detailed healthcare educational
explanation now.
"""

    try:

        return call_llm(
            system_prompt,
            user_prompt
        )

    except Exception as error:

        return (
            "The Explanation Agent could not generate "
            f"the response because of an LLM error: {error}"
        )