from .utils import contains_any


def classify_enquiry(enquiry: str):
    enquiry_lower = enquiry.lower()

    issue_type = "unknown"
    urgency = "low"
    risk_level = "low"
    inspection_recommended = False

    # Water ingress detection
    if contains_any(enquiry_lower, ["damp", "leak", "water", "rain", "moisture"]):
        issue_type = "water_ingress"
        urgency = "medium"
        risk_level = "moderate"
        inspection_recommended = True

    # Electrical issue detection
    if contains_any(enquiry_lower, ["spark", "burning smell", "overheating", "tripping"]):
        issue_type = "electrical_issue"
        urgency = "high"
        risk_level = "high"
        inspection_recommended = True

    return {
        "issue_type": issue_type,
        "urgency": urgency,
        "risk_level": risk_level,
        "inspection_recommended": inspection_recommended
    }
