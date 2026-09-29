def detect_domain(question):
    """Identify the healthcare domain."""

    text = question.lower()

    respiratory = [
        "asthma",
        "breathing",
        "wheezing",
        "cough",
        "lung",
        "respiratory",
        "airway",
        "bronch",
        "smoke"
    ]

    cardiac = [
        "heart",
        "cardiac",
        "blood pressure",
        "hypertension",
        "cholesterol",
        "stroke",
        "pulse",
        "circulation"
    ]

    digestive = [
        "digestive",
        "stomach",
        "acid reflux",
        "heartburn",
        "indigestion",
        "constipation",
        "diarrhea",
        "bowel",
        "gut",
        "abdomen",
        "reflux"
    ]

    if any(word in text for word in respiratory):
        return "RESPIRATORY"

    if any(word in text for word in cardiac):
        return "CARDIAC"

    if any(word in text for word in digestive):
        return "DIGESTIVE"

    return "UNKNOWN"


def detect_topic(question, domain):
    """Identify the main healthcare topic."""

    text = question.lower()

    if domain == "RESPIRATORY":

        if "asthma" in text:
            return "Asthma"

        if "infection" in text:
            return "Respiratory Infections"

        return "Respiratory Health"

    if domain == "CARDIAC":

        if "blood pressure" in text or "hypertension" in text:
            return "Hypertension"

        if "heart" in text:
            return "Heart Health"

        return "Cardiovascular Health"

    if domain == "DIGESTIVE":

        if "acid reflux" in text or "heartburn" in text:
            return "Acid Reflux"

        if "constipation" in text:
            return "Constipation"

        if "diarrhea" in text:
            return "Diarrhea"

        return "Digestive Health"

    return "General Health"


def detect_intent(question):
    """Understand what the user wants to know."""

    text = question.lower()

    if any(
        word in text
        for word in [
            "symptom",
            "symptoms",
            "sign",
            "signs",
            "warning"
        ]
    ):
        return "Symptom Understanding"

    if any(
        word in text
        for word in [
            "cause",
            "causes",
            "trigger",
            "triggers"
        ]
    ):
        return "Causes and Triggers"

    if any(
        word in text
        for word in [
            "treatment",
            "manage",
            "management"
        ]
    ):
        return "Treatment and Management"

    if any(
        word in text
        for word in [
            "prevent",
            "prevention"
        ]
    ):
        return "Prevention"

    if any(
        word in text
        for word in [
            "what is",
            "what are",
            "define",
            "definition"
        ]
    ):
        return "General Explanation"

    if any(
        word in text
        for word in [
            "why",
            "how",
            "when"
        ]
    ):
        return "Educational Explanation"

    return "General Healthcare Information"


def detect_question_type(question):
    """Classify the type of healthcare question."""

    text = question.lower()

    if "symptom" in text or "symptoms" in text:
        return "Symptom Information"

    if "cause" in text or "causes" in text:
        return "Cause Information"

    if "treatment" in text or "management" in text:
        return "Treatment Information"

    if "prevent" in text or "prevention" in text:
        return "Prevention Information"

    if "what is" in text or "what are" in text:
        return "Definition / General Information"

    if "how" in text:
        return "How-to Educational Guidance"

    if "why" in text:
        return "Reason / Explanation"

    return "General Information"


def detect_safety(question):
    """Assign a basic educational safety classification."""

    text = question.lower()

    urgent_words = [
        "emergency",
        "severe",
        "chest pain",
        "trouble breathing",
        "difficulty breathing",
        "fainting",
        "blue lips"
    ]

    if any(word in text for word in urgent_words):
        return "Urgent Clinical Evaluation"

    return "General Educational"


def generate_question(user_question):
    """
    Analyze the healthcare question and create
    structured information for the next agent.
    """

    if not user_question or not user_question.strip():
        raise ValueError("A healthcare question is required.")

    question = user_question.strip()

    domain = detect_domain(question)
    topic = detect_topic(question, domain)
    intent = detect_intent(question)
    question_type = detect_question_type(question)
    safety = detect_safety(question)

    # Detailed analysis that can be passed
    # to the next healthcare agent.
    information_needed = []

    if intent == "Symptom Understanding":
        information_needed = [
            "Definition of the condition",
            "Common symptoms",
            "Typical warning signs",
            "Possible triggers or contributing factors",
            "When professional evaluation may be needed"
        ]

    elif intent == "Causes and Triggers":
        information_needed = [
            "Definition",
            "Common causes",
            "Known triggers",
            "Risk factors",
            "Relevant prevention information"
        ]

    elif intent == "Treatment and Management":
        information_needed = [
            "Definition",
            "General management concepts",
            "Lifestyle or prevention information",
            "When professional medical advice may be needed"
        ]

    elif intent == "Prevention":
        information_needed = [
            "Definition",
            "Risk factors",
            "Prevention strategies",
            "Warning signs"
        ]

    else:
        information_needed = [
            "Definition",
            "Common symptoms",
            "Causes or triggers",
            "Evaluation",
            "Management",
            "Prevention"
        ]

    analysis_summary = (
        f"The user is asking for {intent.lower()} "
        f"information about {topic}. "
        f"The question belongs to the {domain.lower()} "
        f"healthcare domain."
    )

    return {
        "question": question,
        "domain": domain,
        "topic": topic,
        "intent": intent,
        "question_type": question_type,
        "safety_classification": safety,
        "analysis_summary": analysis_summary,
        "information_needed": information_needed
    }