from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse
from sources.workflow.agents_workflow import app
from sources.logger import logging
from sources.exception import CustomException
import sys  

from pydantic import BaseModel
from typing import List, Dict, Optional

app_api = FastAPI()


# -------------------------
# Request Schemas
# -------------------------

class GenerateRequest(BaseModel):
    input: str
    student_id: Optional[int] = 1


class SubmitRequest(BaseModel):
    input: str
    quiz_attempts: List[Dict]
    student_id: Optional[int] = 1


# -------------------------
# Generate Quiz Endpoint
# -------------------------

@app_api.post("/generate")
async def generate_quiz(req: GenerateRequest):
    state = {
        "input": req.input,
        "student_id": req.student_id,
        "quiz_attempts": []  # important for first phase
    }

    result = await app.ainvoke(state)

    return {
        "quiz": result.get("quiz", []),
        "subject": result.get("subject"),
        "topics": result.get("topics")
    }


# -------------------------
# Submit Quiz Endpoint
# -------------------------

@app_api.post("/submit")
async def submit_quiz(req: SubmitRequest):
    state = {
        "input": req.input,
        "student_id": req.student_id,
        "quiz_attempts": req.quiz_attempts
    }

    result = await app.ainvoke(state)

    return {
        "score": result.get("score"),
        "feedback": result.get("feedback"),
        "weak_topic": result.get("weak_topic"),
        "explanation": result.get("explanation")
    }


# # -------------------------
# # Streaming Endpoint (Optional)
# # -------------------------

# from fastapi.responses import StreamingResponse

# def event_stream(state):
#     for chunk in app.stream(state):
#         yield f"data: {chunk}\n\n"


# @app_api.post("/stream")
# def stream(req: GenerateRequest):
#     state = {
#         "input": req.input,
#         "student_id": req.student_id
#     }

#     return StreamingResponse(
#         event_stream(state),
#         media_type="text/event-stream"
#     )

if __name__ == "__main__":
    uvicorn.run(app_api, host="http://[IP_ADDRESS]", port=8000)