import streamlit as st
from medtech_assistant import troubleshoot_issue


st.set_page_config(
    page_title="MedTech AI Support Assistant",
    page_icon="🩺",
    layout="centered"
)


def build_service_note(device_type, result):
    questions_text = "\n".join(f"- {q}" for q in result["questions"])
    steps_text = "\n".join(f"- {s}" for s in result["troubleshooting_steps"])

    return f"""
MEDTECH TECHNICAL SUPPORT REPORT

Device type:
{device_type}

Issue:
{result["issue"]}

Category:
{result["category"]}

Estimated severity:
{result["severity"]}

Recommended action:
{result["recommended_action"]}

Requires human review:
{"Yes" if result["requires_human_review"] else "No"}

Questions to ask customer:
{questions_text}

Safe first-level troubleshooting steps:
{steps_text}

Safety note:
This tool is for first-level technical triage only. It does not replace qualified field service engineering review, clinical judgement, manufacturer procedures, or regulatory safety processes.
"""


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

device_type = st.selectbox(
    "Select device type:",
    [
        "Endoscope tower",
        "Surgical camera",
        "Laser system",
        "Light source",
        "Imaging workstation",
        "Other / unknown"
    ]
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
        full_issue_description = f"{device_type}: {issue_text}"
        result = troubleshoot_issue(full_issue_description)
        service_note = build_service_note(device_type, result)

        st.subheader("Support Report")

        st.write("**Device type:**")
        st.write(device_type)

        st.write("**Issue:**")
        st.write(issue_text)

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
        st.text_area("Copyable internal note:", service_note, height=350)

        st.download_button(
            label="Download Support Report",
            data=service_note,
            file_name="medtech_support_report.txt",
            mime="text/plain"
        )