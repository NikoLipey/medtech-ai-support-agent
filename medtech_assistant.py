def normalise_device_type(device_type):
    if not device_type:
        return "Other / unknown"
    return device_type.strip()


def classify_issue(device_type, issue_text):
    device_type = normalise_device_type(device_type).lower()
    issue_text = issue_text.lower()
    combined_text = f"{device_type} {issue_text}"

    if any(word in combined_text for word in ["image", "monitor", "camera", "black screen", "video"]):
        return "Imaging / video issue"

    if any(word in combined_text for word in ["laser", "output", "calibration", "power meter"]):
        return "Laser output / calibration issue"

    if any(word in combined_text for word in ["software", "crash", "startup", "driver", "windows", "login"]):
        return "Software / workstation issue"

    if any(word in combined_text for word in ["lamp", "light source", "illumination", "brightness"]):
        return "Light source / illumination issue"

    if "endoscope" in device_type:
        return "Endoscopy system issue"

    if "surgical camera" in device_type:
        return "Surgical camera issue"

    if "laser system" in device_type:
        return "Laser system issue"

    if "imaging workstation" in device_type:
        return "Imaging workstation issue"

    return "General technical issue"


def estimate_severity(device_type, issue_text):
    device_type = normalise_device_type(device_type).lower()
    issue_text = issue_text.lower()
    combined_text = f"{device_type} {issue_text}"

    high_risk_words = [
        "surgery",
        "procedure",
        "patient",
        "black screen",
        "no image",
        "injury",
        "burn",
        "smoke",
        "electrical smell",
        "sparking",
        "alarm during procedure",
        "treatment interrupted"
    ]

    medium_risk_words = [
        "weak",
        "intermittent",
        "output",
        "calibration",
        "crash",
        "startup",
        "error message",
        "driver",
        "lamp",
        "brightness"
    ]

    for word in high_risk_words:
        if word in combined_text:
            return "High"

    if "laser system" in device_type and any(word in issue_text for word in ["output", "weak", "calibration", "inconsistent"]):
        return "Medium"

    for word in medium_risk_words:
        if word in combined_text:
            return "Medium"

    return "Low"


def triage_ticket(severity):
    if severity == "High":
        return "Escalate immediately"
    elif severity == "Medium":
        return "Investigate within normal service workflow"
    else:
        return "Handle as low-priority support case"


def requires_human_review(device_type, issue_text, severity):
    device_type = normalise_device_type(device_type).lower()
    issue_text = issue_text.lower()
    combined_text = f"{device_type} {issue_text}"

    safety_words = [
        "surgery",
        "procedure",
        "patient",
        "black screen",
        "no image",
        "laser",
        "burn",
        "injury",
        "smoke",
        "sparking",
        "treatment interrupted"
    ]

    if severity == "High":
        return True

    if "laser system" in device_type:
        return True

    for word in safety_words:
        if word in combined_text:
            return True

    return False


def generate_customer_questions(device_type, issue_category):
    device_type = normalise_device_type(device_type)

    if device_type == "Endoscope tower" or issue_category == "Imaging / video issue":
        return [
            "When did the image issue first occur?",
            "Does the problem happen continuously or intermittently?",
            "Have you tested another video cable or monitor?",
            "Does the camera head show any visible damage?",
            "Was the issue observed during a clinical procedure?"
        ]

    if device_type == "Surgical camera":
        return [
            "Is the issue present with one camera head or multiple camera heads?",
            "Does the issue occur with different video cables?",
            "Is the image absent, distorted, flickering, or intermittent?",
            "Are there any error messages on the camera control unit?",
            "Was the issue observed during a clinical procedure?"
        ]

    if device_type == "Laser system":
        return [
            "When was the laser system last calibrated or serviced?",
            "Are there any warning messages, alarms, or error codes?",
            "Has output been checked with a suitable power meter by qualified personnel?",
            "Were the optics recently cleaned, adjusted, or replaced?",
            "Did the issue appear suddenly or gradually?"
        ]

    if device_type == "Light source":
        return [
            "Does the lamp or LED module turn on?",
            "Are there any warning indicators or error messages?",
            "Is the brightness reduced or completely absent?",
            "Has the lamp/module reached end-of-life hours?",
            "Have you tested the light cable or another compatible light source?"
        ]

    if device_type == "Imaging workstation":
        return [
            "What error message appears on screen?",
            "Did the issue begin after a software, driver, or Windows update?",
            "Does the crash happen every time or only occasionally?",
            "What software version is installed?",
            "Has the workstation been restarted?"
        ]

    return [
        "What is the device model and serial number?",
        "When did the issue start?",
        "Are there any error messages?",
        "Has anything changed recently in setup, software, cables, accessories, or maintenance?",
        "Is the issue affecting clinical workflow or patient safety?"
    ]


def recommend_troubleshooting(device_type, issue_category):
    device_type = normalise_device_type(device_type)

    if device_type == "Endoscope tower" or issue_category == "Imaging / video issue":
        return [
            "Check video cable connections",
            "Check camera head connection",
            "Test with another monitor if available",
            "Confirm the correct input/source is selected on the monitor",
            "Escalate if the issue occurs during a clinical procedure"
        ]

    if device_type == "Surgical camera":
        return [
            "Check camera head connection to the control unit",
            "Inspect external cable condition",
            "Test with another compatible monitor or video input if available",
            "Record any error messages from the camera control unit",
            "Escalate if image loss is intermittent or procedure-impacting"
        ]

    if device_type == "Laser system":
        return [
            "Confirm the system is in the correct treatment/settings mode",
            "Check for visible warning messages or error codes",
            "Confirm calibration status according to local procedures",
            "Inspect external optics only if permitted by the manufacturer procedure",
            "Escalate to qualified service personnel if output remains inconsistent or below specification"
        ]

    if device_type == "Light source":
        return [
            "Check power connection and standby/active status",
            "Check lamp or LED module status indicators",
            "Inspect the external light cable for visible damage",
            "Try a known compatible light cable or light source if available",
            "Escalate if module replacement or internal inspection is required"
        ]

    if device_type == "Imaging workstation":
        return [
            "Record the exact error message",
            "Restart the workstation",
            "Check recent software, driver, or operating system updates",
            "Verify system compatibility and connected peripherals",
            "Escalate if the crash repeats or affects clinical workflow"
        ]

    return [
        "Collect device model and serial number",
        "Ask when the issue started",
        "Check for error messages",
        "Check recent changes or maintenance",
        "Escalate if patient safety or clinical workflow is affected"
    ]


def troubleshoot_issue(device_type, issue_text=None):
    """
    Device-aware technical triage function.

    Supports both:
    troubleshoot_issue(device_type, issue_text)
    and the old v1.0/v1.1 style:
    troubleshoot_issue(issue_text)
    """

    if issue_text is None:
        issue_text = device_type
        device_type = "Other / unknown"

    device_type = normalise_device_type(device_type)

    category = classify_issue(device_type, issue_text)
    severity = estimate_severity(device_type, issue_text)
    action = triage_ticket(severity)
    human_review = requires_human_review(device_type, issue_text, severity)
    questions = generate_customer_questions(device_type, category)
    steps = recommend_troubleshooting(device_type, category)

    return {
        "device_type": device_type,
        "issue": issue_text,
        "category": category,
        "severity": severity,
        "recommended_action": action,
        "requires_human_review": human_review,
        "questions": questions,
        "troubleshooting_steps": steps
    }
