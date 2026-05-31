
import streamlit as st
from medtech_assistant import troubleshoot_issue

st.set_page_config(
    page_title="MedTech AI Support Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("MedTech Technical Support Assistant")

st.write(
    """
    This prototype helps triage MedTech device support issues.
    It classifies the issue, estimates severity, recommends escalation,
    generates customer questions, and proposes safe first-level troubleshooting steps.
    """
)

st.warning(
    "This tool is for first-level technical triage only. It does not replace qualified field service engineering review or clinical safety procedures."
)

issue_text = st.text_area(
    "Describe the device issue:",
    placeholder="Example: The endoscope tower shows no image during a procedure and the monitor is black.",
    height=150
)

if st.button("Generate Support Report"):
    if not issue_text.strip():
        st.error("Please enter a device issue description.")
    else:
        result = troubleshoot_issue(issue_text)

        st.subheader("Support Report")

        st.write("**Issue:**")
        st.write(result["issue"])

        st.write("**Category:**")
        st.write(result["category"])

        st.write("**Estimated severity:**")
        st.write(result["severity"])

        st.write("**Recommended action:**")
        st.write(result["recommended_action"])

        st.write("**Requires human review:**")
        st.write("Yes" if result["requires_human_review"] else "No")

        st.subheader("Questions to Ask the Customer")
        for question in result["questions"]:
            st.write(f"- {question}")

        st.subheader("Safe First-Level Troubleshooting Steps")
        for step in result["troubleshooting_steps"]:
            st.write(f"- {step}")

        st.subheader("Internal Service Note")

        service_note = f"""
Issue: {result["issue"]}

Category: {result["category"]}

Estimated severity: {result["severity"]}

Recommended action: {result["recommended_action"]}

Requires human review: {"Yes" if result["requires_human_review"] else "No"}

Questions to ask customer:
{chr(10).join("- " + q for q in result["questions"])}

Troubleshooting steps:
{chr(10).join("- " + s for s in result["troubleshooting_steps"])}
"""

        st.text_area("Copyable internal note:", service_note, height=300)
