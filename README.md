# Lead Response Assistant

## Overview

This project is a structured Lead Response Assistant that reads a customer enquiry and generates a safe and helpful draft reply.

The system is designed to be reliable and explainable.  
Instead of relying on a generative chatbot, it uses clear rule-based logic and structured reasoning to avoid hallucinated claims.

---

## Key Features

- Deterministic issue classification (rule-based)
- Structured reasoning engine
- Logical merging of enquiry, inspection, and thermal data
- Conflict handling with confidence adjustment
- Controlled knowledge base for approved next steps
- Separate response generation layer
- Final safety guardrail check

---

## System Architecture

The system follows a layered approach:

1. **Classifier**
   - Detects issue type, urgency, and risk level using keyword rules.

2. **Reasoning Engine**
   - Builds a structured `case_object`
   - Merges inspection and thermal data
   - Detects conflicting information
   - Adjusts confidence score
   - Stores reasoning trace for transparency

3. **Knowledge Base**
   - Provides clarification questions
   - Provides approved safe next steps

4. **Response Generator**
   - Converts the structured case object into a natural draft response
   - Does not perform reasoning

5. **Guardrails**
   - Scans final response for risky phrases (e.g., guarantees)
   - Blocks unsafe output

This separation ensures explainability and reduces hallucination risk.

---

## How It Handles Evaluation Criteria

- **Accuracy of Extracted Information**
  - Deterministic keyword-based classification

- **Logical Merging of Inspection + Thermal Data**
  - Structured signal merging inside reasoning engine

- **Handling Missing / Conflicting Details**
  - Adds clarification questions
  - Lowers confidence when conflicts are detected
  - Logs reasoning trace

- **Clarity of Final Output**
  - Structured draft diagnostic response
  - Clear next steps and questions

- **System Thinking & Reliability**
  - Separation of reasoning and response generation
  - Controlled knowledge base
  - Safety validation layer

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```
2. Start the server:
```bash
uvicorn app:app --reload
```
3. Open Swagger UI:
```bash
http://127.0.0.1:8000/docs
```
4. Use POST /generate-reply to test.

## Example Input
```bash
{
  "enquiry": "Damp patches on bedroom wall after rain.",
  "inspection_data": {
    "external_cracks": true
  },
  "thermal_data": {
    "cold_bridge_detected": true
  }
}
```
## Example output
```bash
{
  "case_object": {
    "original_enquiry": "Damp patches on bedroom wall after rain.",
    "issue_type": "water_ingress",
    "urgency": "medium",
    "risk_level": "moderate",
    "inspection_recommended": true,
    "clarification_questions": [
      "Is the affected wall an external wall?",
      "Does the damp appear only after heavy rainfall?",
      "Have you noticed cracks or issues with gutters externally?",
      "Is there any mould smell or visible mould growth?"
    ],
    "safe_next_steps": [
      "Check gutters and downpipes for visible blockages",
      "Inspect the external wall for visible cracks",
      "Take clear photographs of the affected area",
      "Monitor whether the damp worsens after rainfall"
    ],
    "confidence": 0.85,
    "identified_signals": [
      "external_cracks_detected",
      "cold_bridge_pattern",
      "localized_moisture_pattern",
      "rain_trigger",
      "visible_moisture"
    ],
    "reasoning_trace": [
      "Inspection data indicates external cracking.",
      "Thermal imaging shows cold bridging.",
      "Conflicting signals: good roof condition but cold bridging detected.",
      "Matched issue_type 'water_ingress' to knowledge base."
    ],
    "missing_data_flag": true
  },
  "reply": "Hi there,\n\nThank you for getting in touch. Damp patches appearing after rainfall can understandably be worrying.\n\nTo help us better understand what's happening, could you please clarify:\n- Is the affected wall an external wall?\n- Does the damp appear only after heavy rainfall?\n- Have you noticed cracks or issues with gutters externally?\n- Is there any mould smell or visible mould growth?\n\nIn the meantime, you may consider the following:\n- Check gutters and downpipes for visible blockages\n- Inspect the external wall for visible cracks\n- Take clear photographs of the affected area\n- Monitor whether the damp worsens after rainfall\n\n\nOnce we have a bit more information, we’ll be able to guide you on the most appropriate next steps."
}
```
## Limitations

Classification is keyword-based and may miss complex language.

Knowledge base is limited in scope.

Confidence scoring is rule-based.

Does not automatically process full inspection documents.

## Future Improvements

With more time, the system could be improved by:

Using AI for better language understanding

Automatically extracting structured data from inspection reports

Improving confidence scoring with weighted signals

Expanding the knowledge base

## Design Philosophy

The system prioritises:

Reliability over guessing

Explainability over complexity

Structured reasoning over pure generation

The goal is to build a safe and production-ready decision support system.