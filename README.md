
# MedTech Technical Support Assistant

This is a prototype AI-style technical support assistant for MedTech device issue triage.

## Purpose

The tool helps first-level support teams analyse device issue descriptions and produce a structured support report.

## Features

- Classifies the issue type
- Estimates severity
- Recommends escalation
- Flags whether human review is required
- Generates questions to ask the customer
- Suggests safe first-level troubleshooting steps
- Produces a copyable internal service note

## Example Use Case

Input:

"The endoscope tower shows no image during a procedure and the monitor is black."

Output:

- Category: Imaging / video issue
- Severity: High
- Recommended action: Escalate immediately
- Requires human review: Yes
- Customer questions
- Troubleshooting checklist
- Internal service note

## Safety Note

This tool is for first-level technical triage only. It does not replace qualified field service engineering review, clinical judgement, manufacturer procedures, or regulatory safety processes.

## Tech Stack

- Python
- Streamlit
- Rule-based logic
- Future upgrade: LLM-generated support response and document retrieval
