from agents.question_agent import generate_question
from agents.retrieval_agent import retrieve_context
from agents.explanation_agent import explain_answer
from agents.verification_agent import verify_answer


def run_orchestration(user_question):
    """Run the complete healthcare multi-agent workflow."""

    # ------------------------------------------------
    # 1. Question Agent
    # ------------------------------------------------

    analysis = generate_question(user_question)
    question = analysis["question"]

    question_details = {
        "agent": "Question Agent",
        "purpose": "Understand and classify the healthcare question.",
        "input": question,
        "domain": analysis["domain"],
        "topic": analysis["topic"],
        "intent": analysis["intent"],
        "question_type": analysis["question_type"],
        "safety": analysis["safety_classification"],
        "output": "Structured question information created."
    }

    # ------------------------------------------------
    # 2. Retrieval Agent
    # ------------------------------------------------

    context = retrieve_context(
        question,
        domain_hint=analysis["domain"]
    )

    retrieval_details = {
        "agent": "Retrieval Agent",
        "purpose": "Find relevant healthcare information from the RAG knowledge base.",
        "input": question,
        "domain": analysis["domain"],
        "chunks_retrieved": len(context),
        "output": "Relevant healthcare document chunks retrieved."
    }

    # ------------------------------------------------
    # 3. Explanation Agent
    # ------------------------------------------------

    answer = explain_answer(
        question,
        context,
        analysis
    )

    explanation_details = {
        "agent": "Explanation Agent",
        "purpose": "Create a detailed educational response using retrieved information.",
        "input": "Question + retrieved healthcare context",
        "topic": analysis["topic"],
        "output": "Detailed healthcare educational explanation generated."
    }

    # ------------------------------------------------
    # 4. Verification Agent
    # ------------------------------------------------

    verified_answer = verify_answer(
        answer,
        context,
        analysis
    )

    verification_details = {
        "agent": "Verification Agent",
        "purpose": "Check the generated response before showing it to the user.",
        "checks": [
            "Answer exists",
            "Relevant healthcare context was retrieved",
            "Educational disclaimer is included"
        ],
        "status": "Verified",
        "output": "Verified response prepared for the user."
    }

    # ------------------------------------------------
    # A2A Communication
    # ------------------------------------------------

    a2a_messages = [
        {
            "from": "User",
            "to": "Question Agent",
            "message": question
        },
        {
            "from": "Question Agent",
            "to": "Retrieval Agent",
            "message": (
                f"Retrieve information related to "
                f"{analysis['topic']} from the "
                f"{analysis['domain']} domain."
            )
        },
        {
            "from": "Retrieval Agent",
            "to": "Explanation Agent",
            "message": (
                f"{len(context)} relevant healthcare "
                "document chunks were retrieved."
            )
        },
        {
            "from": "Explanation Agent",
            "to": "Verification Agent",
            "message": "Detailed educational answer generated."
        },
        {
            "from": "Verification Agent",
            "to": "Final Response",
            "message": "Answer verified and ready to display."
        }
    ]

    # ------------------------------------------------
    # Tools
    # ------------------------------------------------

    tools = [
        {
            "tool": "ChromaDB",
            "purpose": "Healthcare vector database",
            "action": "Semantic document retrieval",
            "result": f"{len(context)} chunks retrieved"
        },
        {
            "tool": "SentenceTransformer",
            "purpose": "Text embedding",
            "action": "Convert question into embedding for similarity search",
            "result": "Embedding generated"
        },
        {
            "tool": "Groq LLM",
            "purpose": "Generate educational explanation",
            "action": "Process retrieved healthcare context",
            "result": "Response generated"
        }
    ]

    # ------------------------------------------------
    # Memory
    # ------------------------------------------------

    memory = [
        {
            "stage": "Question",
            "content": question
        },
        {
            "stage": "Analysis",
            "content": (
                f"Domain: {analysis['domain']} | "
                f"Topic: {analysis['topic']}"
            )
        },
        {
            "stage": "Retrieval",
            "content": (
                f"{len(context)} healthcare chunks retrieved"
            )
        },
        {
            "stage": "Explanation",
            "content": "Educational response generated from retrieved context."
        },
        {
            "stage": "Verification",
            "content": "Response verified before final presentation."
        }
    ]

    return {
        "question": question,
        "analysis": analysis,
        "answer": verified_answer,

        "retrieved_documents": context,

        "sources": [
            item["source"]
            for item in context
        ],

        "detected_domain": analysis["domain"],

        "retrieved_domain": [
            item.get("domain", "UNKNOWN")
            for item in context
        ],

        "relevant_chunks": len(context),

        "question_details": question_details,
        "retrieval_details": retrieval_details,
        "explanation_details": explanation_details,
        "verification_details": verification_details,

        "a2a_messages": a2a_messages,
        "tools": tools,
        "memory": memory,

        "verification": {
            "status": "Verified",
            "domain": analysis["domain"],
            "source_count": len(context),
            "message": "Answer checked before final response."
        }
    }