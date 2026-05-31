
def classify_issue(issue_text):
    issue_text = issue_text.lower()

    if "image" in issue_text or "monitor" in issue_text or "camera" in issue_text:
        return "Imaging / video issue"
    elif "laser" in issue_text or "output" in issue_text:
        return "Laser output issue"
    elif "software" in issue_text or "crash" in issue_text or "startup" in issue_text:
        return "Software issue"
    elif "lamp" in issue_text or "light" in issue_text:
        return "Light source issue"
    else:
        return "General technical issue"


def estimate_severity(issue_text):
    issue_text = issue_text.lower()

    high_risk_words = ["surgery", "procedure", "no image", "black screen", "patient", "intermittent"]
    medium_risk_words = ["weak", "output", "crash", "startup", "calibration"]

    for word in high_risk_words:
        if word in issue_text:
            return "High"

    for word in medium_risk_words:
        if word in issue_text:
            return "Medium"

    return "Low"


def triage_ticket(severity):
    if severity == "High":
        return "Escalate immediately"
    elif severity == "Medium":
        return "Investigate within normal service workflow"
    else:
        return "Handle as low-priority support case"


def requires_human_review(issue_text, severity):
    issue_text = issue_text.lower()

    safety_words = ["surgery", "procedure", "patient", "black screen", "no image", "laser", "burn", "injury"]

    if severity == "High":
        return True

    for word in safety_words:
        if word in issue_text:
            return True

    return False


def generate_customer_questions(issue_category):
    if issue_category == "Imaging / video issue":
        return [
            "When did the image issue first occur?",
            "Does the problem happen continuously or intermittently?",
            "Have you tested another video cable or monitor?",
            "Does the camera head show any visible damage?",
            "Was the issue observed during a clinical procedure?"
        ]

    elif issue_category == "Laser output issue":
        return [
            "When was the laser system last calibrated?",
            "Are there any error messages on the system?",
            "Has the output been measured with a power meter?",
            "Were the optics recently cleaned or replaced?",
            "Did the issue appear suddenly or gradually?"
        ]

    elif issue_category == "Software issue":
        return [
            "What error message appears on screen?",
            "Did the issue begin after a software or Windows update?",
            "Does the crash happen every time or only occasionally?",
            "What software version is installed?",
            "Has the workstation been restarted?"
        ]

    else:
        return [
            "What is the device model and serial number?",
            "When did the issue start?",
            "Are there any error messages?",
            "Has anything changed recently in setup, software, cables or accessories?",
            "Is the issue affecting clinical workflow or patient safety?"
        ]


def recommend_troubleshooting(issue_category):
    if issue_category == "Imaging / video issue":
        return [
            "Check video cable connections",
            "Check camera head connection",
            "Test with another monitor if available",
            "Restart the imaging system if safe to do so",
            "Escalate if issue occurs during clinical procedure"
        ]

    elif issue_category == "Laser output issue":
        return [
            "Check whether optics are clean",
            "Verify calibration status",
            "Check system error messages",
            "Confirm correct treatment/settings mode",
            "Escalate if output remains below specification"
        ]

    elif issue_category == "Software issue":
        return [
            "Record the error message",
            "Restart the workstation",
            "Check recent software or driver updates",
            "Verify system compatibility",
            "Escalate if crash repeats"
        ]

    elif issue_category == "Light source issue":
        return [
            "Check power connection",
            "Check lamp module",
            "Inspect error indicators",
            "Try a known working lamp module if available",
            "Escalate if replacement does not resolve the issue"
        ]

    else:
        return [
            "Collect device model and serial number",
            "Ask when the issue started",
            "Check for error messages",
            "Check recent changes or maintenance",
            "Escalate if patient safety or clinical workflow is affected"
        ]


def troubleshoot_issue(issue_text):
    category = classify_issue(issue_text)
    severity = estimate_severity(issue_text)
    action = triage_ticket(severity)
    human_review = requires_human_review(issue_text, severity)
    questions = generate_customer_questions(category)
    steps = recommend_troubleshooting(category)

    return {
        "issue": issue_text,
        "category": category,
        "severity": severity,
        "recommended_action": action,
        "requires_human_review": human_review,
        "questions": questions,
        "troubleshooting_steps": steps
    }
