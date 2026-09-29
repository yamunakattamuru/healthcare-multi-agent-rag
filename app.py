import streamlit as st
from core.orchestrator import run_orchestration


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Healthcare FAQ",
    page_icon="🏥",
    layout="wide"
)


# --------------------------------------------------
# HEALTHCARE KNOWLEDGE BASE
# --------------------------------------------------

DOMAINS = {
    "🫁 Respiratory": [
        "asthma.txt",
        "common_respiratory_infections.txt",
        "respiratory_health.txt"
    ],
    "❤️ Cardiac": [
        "hypertension.txt",
        "heart_health.txt",
        "cardiovascular_risk_factors.txt"
    ],
    "🩺 Digestive": [
        "acid_reflux.txt",
        "digestive_health.txt",
        "common_digestive_conditions.txt"
    ]
}


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏥 HEALTHCARE FAQ")

st.caption(
    "Multi-Agent RAG System | "
    "Synthetic Educational Healthcare Knowledge Base"
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📚 Knowledge Base")

    for domain, files in DOMAINS.items():

        st.markdown(f"**{domain}**")

        for file in files:
            st.write(f"📄 {file}")

    st.divider()

    st.info(
        "This application provides synthetic educational "
        "healthcare information for a hackathon demonstration."
    )


# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

st.subheader("Ask a Healthcare Question")

question = st.text_area(
    "Question",
    placeholder="Example: What are common symptoms of asthma?",
    height=100,
    label_visibility="collapsed"
)


# --------------------------------------------------
# GENERATE ANSWER
# --------------------------------------------------

if st.button(
    "🚀 Generate Answer",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a healthcare question."
        )

    else:

        with st.spinner(
            "Running Question → Retrieval → "
            "Explanation → Verification..."
        ):

            try:

                result = run_orchestration(question)

                st.session_state["result"] = result

            except Exception as error:

                st.error(
                    "Something went wrong while "
                    "running the healthcare agents."
                )

                st.exception(error)


# --------------------------------------------------
# GET RESULT
# --------------------------------------------------

result = st.session_state.get("result")


if result:

    tabs = st.tabs([
        "🎯 Orchestration",
        "🔄 A2A Messages",
        "📚 RAG / Vector DB",
        "🛠️ Tools",
        "🧠 Memory",
        "✅ Verification",
        "📄 Final Response"
    ])


    # ==================================================
    # TAB 1 — ORCHESTRATION
    # ==================================================

    with tabs[0]:

        st.subheader(
            "🎯 Healthcare Agent Orchestration"
        )

        st.write(
            "The Orchestrator coordinates four "
            "specialized agents to understand the "
            "question, retrieve evidence, generate "
            "an explanation, and verify the response."
        )

        st.divider()


        # ----------------------------------------------
        # QUESTION AGENT
        # ----------------------------------------------

        st.subheader(
            "🧠 1. Question Agent"
        )

        q = result.get(
            "question_details",
            {}
        )

        st.write(
            "**Purpose:**",
            q.get(
                "purpose",
                ""
            )
        )

        st.write(
            "**Input:**",
            q.get(
                "input",
                ""
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Domain",
                q.get(
                    "domain",
                    "UNKNOWN"
                )
            )

        with col2:

            st.metric(
                "Topic",
                q.get(
                    "topic",
                    "Unknown"
                )
            )

        with col3:

            st.metric(
                "Intent",
                q.get(
                    "intent",
                    "Unknown"
                )
            )

        st.write(
            "**Question Type:**",
            q.get(
                "question_type",
                "Unknown"
            )
        )

        st.write(
            "**Safety Classification:**",
            q.get(
                "safety",
                "Unknown"
            )
        )

        st.write(
            "**Output:**",
            q.get(
                "output",
                ""
            )
        )

        st.divider()


        # ----------------------------------------------
        # RETRIEVAL AGENT
        # ----------------------------------------------

        st.subheader(
            "📚 2. Retrieval Agent"
        )

        r = result.get(
            "retrieval_details",
            {}
        )

        st.write(
            "**Purpose:**",
            r.get(
                "purpose",
                ""
            )
        )

        st.write(
            "**Domain searched:**",
            r.get(
                "domain",
                "UNKNOWN"
            )
        )

        st.metric(
            "Relevant Chunks Retrieved",
            r.get(
                "chunks_retrieved",
                0
            )
        )

        st.write(
            "**Output:**",
            r.get(
                "output",
                ""
            )
        )

        st.divider()


        # ----------------------------------------------
        # EXPLANATION AGENT
        # ----------------------------------------------

        st.subheader(
            "💬 3. Explanation Agent"
        )

        e = result.get(
            "explanation_details",
            {}
        )

        st.write(
            "**Purpose:**",
            e.get(
                "purpose",
                ""
            )
        )

        st.write(
            "**Input:**",
            e.get(
                "input",
                ""
            )
        )

        st.write(
            "**Topic:**",
            e.get(
                "topic",
                ""
            )
        )

        st.write(
            "**Output:**",
            e.get(
                "output",
                ""
            )
        )

        st.divider()


        # ----------------------------------------------
        # VERIFICATION AGENT
        # ----------------------------------------------

        st.subheader(
            "✅ 4. Verification Agent"
        )

        v = result.get(
            "verification_details",
            {}
        )

        st.write(
            "**Purpose:**",
            v.get(
                "purpose",
                ""
            )
        )

        st.write(
            "**Checks performed:**"
        )

        for check in v.get(
            "checks",
            []
        ):

            st.write(
                f"✓ {check}"
            )

        st.success(
            v.get(
                "output",
                "Verification completed."
            )
        )

        st.divider()


        # ----------------------------------------------
        # ORCHESTRATION SUMMARY
        # ----------------------------------------------

        st.subheader(
            "📊 Orchestration Summary"
        )

        st.write(
            f"**Question:** "
            f"{result.get('question', '')}"
        )

        st.write(
            f"**Detected Domain:** "
            f"{result.get('detected_domain', 'UNKNOWN')}"
        )

        st.write(
            f"**Retrieved Chunks:** "
            f"{result.get('relevant_chunks', 0)}"
        )

        st.write(
            "**Workflow:** "
            "Question → Retrieval → Explanation → "
            "Verification → Final Response"
        )


    # ==================================================
    # TAB 2 — A2A MESSAGES
    # ==================================================

    with tabs[1]:

        st.subheader(
            "🔄 Agent-to-Agent Messages"
        )

        st.write(
            "This tab shows how information moves "
            "between the healthcare agents."
        )

        messages = result.get(
            "a2a_messages",
            []
        )

        if messages:

            for index, message in enumerate(
                messages,
                1
            ):

                sender = message.get(
                    "from",
                    "Unknown"
                )

                receiver = message.get(
                    "to",
                    "Unknown"
                )

                content = message.get(
                    "message",
                    ""
                )

                st.markdown(
                    f"### {index}. "
                    f"{sender} → {receiver}"
                )

                st.info(
                    content
                )

        else:

            st.warning(
                "No A2A messages were recorded."
            )


    # ==================================================
    # TAB 3 — RAG
    # ==================================================

    with tabs[2]:

        st.subheader(
            "📚 RAG / Vector Database"
        )

        st.write(
            "The Retrieval Agent searches the local "
            "healthcare knowledge base using semantic "
            "similarity."
        )

        documents = result.get(
            "retrieved_documents",
            []
        )

        if documents:

            st.success(
                f"{len(documents)} relevant "
                "document chunks retrieved."
            )

            for index, item in enumerate(
                documents,
                1
            ):

                source = item.get(
                    "source",
                    "Unknown"
                )

                domain = item.get(
                    "domain",
                    "Unknown"
                )

                path = item.get(
                    "path",
                    "Unknown"
                )

                with st.expander(
                    f"📄 {index}. {source}"
                ):

                    st.write(
                        f"**Domain:** {domain}"
                    )

                    st.write(
                        f"**Path:** `{path}`"
                    )

                    st.write(
                        item.get(
                            "content",
                            ""
                        )
                    )

        else:

            st.warning(
                "No healthcare documents were retrieved."
            )


    # ==================================================
    # TAB 4 — TOOLS
    # ==================================================

    with tabs[3]:

        st.subheader(
            "🛠️ Tools Used"
        )

        st.write(
            "The healthcare system uses these "
            "components during processing."
        )

        tools = result.get(
            "tools",
            []
        )

        if tools:

            for tool in tools:

                st.markdown(
                    f"### 🔧 "
                    f"{tool.get('tool', 'Tool')}"
                )

                st.write(
                    f"**Purpose:** "
                    f"{tool.get('purpose', 'N/A')}"
                )

                st.write(
                    f"**Action:** "
                    f"{tool.get('action', 'N/A')}"
                )

                st.success(
                    tool.get(
                        "result",
                        "Completed"
                    )
                )

        else:

            st.info(
                "No tools were recorded."
            )


    # ==================================================
    # TAB 5 — MEMORY
    # ==================================================

    with tabs[4]:

        st.subheader(
            "🧠 Session Memory"
        )

        st.write(
            "The system keeps track of important "
            "information from each stage of the "
            "current question."
        )

        memory = result.get(
            "memory",
            []
        )

        if memory:

            for item in memory:

                st.markdown(
                    f"### "
                    f"{item.get('stage', 'Stage')}"
                )

                st.write(
                    item.get(
                        "content",
                        ""
                    )
                )

                st.divider()

        else:

            st.info(
                "No memory information available."
            )


    # ==================================================
    # TAB 6 — VERIFICATION
    # ==================================================

    with tabs[5]:

        st.subheader(
            "✅ Verification Agent"
        )

        verification = result.get(
            "verification",
            {}
        )

        status = verification.get(
            "status",
            "Unknown"
        )

        if status == "Verified":

            st.success(
                "✅ Answer verified successfully."
            )

        else:

            st.warning(
                f"Verification status: {status}"
            )

        st.write(
            f"**Domain:** "
            f"{verification.get('domain', 'UNKNOWN')}"
        )

        st.write(
            f"**Retrieved Sources:** "
            f"{verification.get('source_count', 0)}"
        )

        st.info(
            verification.get(
                "message",
                "Verification completed."
            )
        )


    # ==================================================
    # TAB 7 — FINAL RESPONSE
    # ==================================================

    with tabs[6]:

        st.subheader(
            "📄 Healthcare Educational Response"
        )

        st.success(
            "Final response generated by the "
            "multi-agent healthcare system."
        )

        st.markdown(
            result.get(
                "answer",
                "No answer generated."
            )
        )

        st.divider()

        st.subheader(
            "📚 Sources"
        )

        sources = result.get(
            "sources",
            []
        )

        if sources:

            for source in sources:

                st.write(
                    f"• {source}"
                )

        else:

            st.write(
                "No sources available."
            )
