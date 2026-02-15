import json


class ReasoningEngine:
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        with open(knowledge_base_path, "r") as f:
            self.knowledge_base = json.load(f)

    def build_case_object(self, enquiry, classification,inspection_data=None,thermal_data=None):
        issue_type = classification["issue_type"]

        case = {
            "original_enquiry": enquiry,
            "issue_type": issue_type,
            "urgency": classification["urgency"],
            "risk_level": classification["risk_level"],
            "inspection_recommended": classification["inspection_recommended"],
            "clarification_questions": [],
            "safe_next_steps": [],
            "confidence": 0.0,
            "identified_signals": [],
            "reasoning_trace": [],
            "missing_data_flag": False
        }

        enquiry_lower = enquiry.lower()

        inspection_data = inspection_data or {}
        thermal_data = thermal_data or {}

        # Merge inspection signals
        if inspection_data.get("external_cracks"):
            case["identified_signals"].append("external_cracks_detected")
            case["reasoning_trace"].append(
                "Inspection data indicates external cracking."
            )

        if inspection_data.get("roof_condition") == "poor":
            case["identified_signals"].append("roof_degradation")
            case["urgency"] = "high"
            case["reasoning_trace"].append(
                "Poor roof condition elevates risk level."
            )

        # Merge thermal signals
        if thermal_data.get("cold_bridge_detected"):
            case["identified_signals"].append("cold_bridge_pattern")
            case["reasoning_trace"].append(
                "Thermal imaging shows cold bridging."
            )

        if thermal_data.get("moisture_pattern") == "upper_corner":
            case["identified_signals"].append("localized_moisture_pattern")

        # Conflict example
        if (
            inspection_data.get("roof_condition") == "good"
            and thermal_data.get("cold_bridge_detected")
        ):
            case["confidence"] -= 0.2
            case["reasoning_trace"].append(
                "Conflicting signals: good roof condition but cold bridging detected."
            )

        

        if "rain" in enquiry_lower:
            case["identified_signals"].append("rain_trigger")
        if "damp" in enquiry_lower:
            case["identified_signals"].append("visible_moisture")

        if issue_type in self.knowledge_base:
            kb_data = self.knowledge_base[issue_type]
            case["clarification_questions"] = kb_data["clarification_questions"]
            case["safe_next_steps"] = kb_data["safe_next_steps"]
            case["confidence"] = 0.85
            case["reasoning_trace"].append(
                f"Matched issue_type '{issue_type}' to knowledge base."
            )
        else:
            case["confidence"] = 0.4
            case["reasoning_trace"].append(
                "No direct knowledge base match found."
            )

        if len(case["clarification_questions"]) > 0:
            case["missing_data_flag"] = True

        if "collapse" in enquiry_lower:
            case["urgency"] = "high"
            case["risk_level"] = "high"
            case["reasoning_trace"].append(
                "Detected structural keyword 'collapse' → elevated urgency."
            )

        return case
