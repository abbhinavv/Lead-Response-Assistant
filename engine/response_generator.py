def generate_response(case_object):

    if case_object["issue_type"] == "unknown":
        return (
            "Thanks for reaching out. "
            "Could you please share a bit more detail about what you're experiencing so we can guide you appropriately?"
        )

    # Dynamic acknowledgement based on issue
    issue_acknowledgement = {
        "water_ingress": "Damp patches appearing after rainfall can understandably be worrying.",
        "electrical_issue": "Electrical concerns should always be taken seriously.",
    }

    intro_line = issue_acknowledgement.get(
        case_object["issue_type"],
        "I understand this situation can be concerning."
    )

    questions = "\n".join(
        [f"- {q}" for q in case_object["clarification_questions"]]
    )

    steps = "\n".join(
        [f"- {s}" for s in case_object["safe_next_steps"]]
    )

    urgency_note = ""
    if case_object["urgency"] == "high":
        urgency_note = "\n\nGiven the nature of this issue, we recommend addressing it promptly."

    response = f"""
Hi there,

Thank you for getting in touch. {intro_line}

To help us better understand what's happening, could you please clarify:
{questions}

In the meantime, you may consider the following:
{steps}
{urgency_note}

Once we have a bit more information, we’ll be able to guide you on the most appropriate next steps.
"""

    return response.strip()
