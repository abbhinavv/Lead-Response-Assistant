from fastapi import FastAPI
from engine.classifier import classify_enquiry
from engine.reasoning_engine import ReasoningEngine
from engine.response_generator import generate_response
from engine.guardrails import validate_response

app = FastAPI()

reasoning_engine = ReasoningEngine()


@app.post("/generate-reply")
def generate_reply(payload: dict):
    enquiry = payload.get("enquiry", "")
    inspection_data = payload.get("inspection_data", {})
    thermal_data = payload.get("thermal_data", {})

    classification = classify_enquiry(enquiry)

    case_object = reasoning_engine.build_case_object(
        enquiry,
        classification,
        inspection_data,
        thermal_data
    )

    response = generate_response(case_object)

    if not validate_response(response):
        return {"error": "Generated response failed safety validation."}

    return {
        "case_object": case_object,
        "reply": response
    }
