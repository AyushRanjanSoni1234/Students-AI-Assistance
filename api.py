from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse

from sources.workflow.agents_workflow import app
from sources.logger import logging
from sources.exception import CustomException

from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import sys

app_api = FastAPI()

# -------------------------
# Request Schemas
# -------------------------
class GenerateRequest(BaseModel):
    input: str
    mode: Optional[str] = "learn"   # 🔥 IMPORTANT
    student_id: Optional[int] = 1


class SubmitRequest(BaseModel):
    input: str
    quiz: List[Dict]
    user_answers: List[str]
    student_id: Optional[int] = 1


logging.info("✅ Request Schemas initialized")


# -------------------------
# GENERATE (Learn + Quiz)
# -------------------------
@app_api.post("/generate")
async def generate(req: GenerateRequest):
    try:
        logging.info(f"📥 /generate | mode={req.mode} | input={req.input}")

        state = {
            "input": req.input,
            "student_id": req.student_id,
            "mode": req.mode,   # 🔥 dynamic mode
            "request_id": str(uuid.uuid4())
        }

        result = await app.ainvoke(state)

        if not result:
            raise ValueError("Empty response from workflow")

        # -------------------------
        # Mode-based response
        # -------------------------
        if req.mode == "learn":
            return {
                "explanation": result.get("explanation"),
                "subject": result.get("subject"),
                "topics": result.get("topics")
            }

        elif req.mode == "quiz_generate":
            if not result.get("quiz"):
                raise ValueError("Quiz not generated")

            return {
                "quiz": result.get("quiz"),
                "subject": result.get("subject"),
                "topics": result.get("topics")
            }

        else:
            raise ValueError(f"Invalid mode: {req.mode}")

    except Exception as e:
        logging.error(f"🔥 Error in /generate: {str(e)}")
        raise CustomException(e, sys)


# -------------------------
# SUBMIT QUIZ
# -------------------------
@app_api.post("/submit")
async def submit(req: SubmitRequest):
    try:
        logging.info("📥 /submit called")

        # basic validation
        if not req.quiz or not req.user_answers:
            raise ValueError("Quiz or answers missing")

        if len(req.quiz) != len(req.user_answers):
            raise ValueError("Mismatch between quiz and answers")

        state = {
            "input": req.input,
            "student_id": req.student_id,
            "quiz": req.quiz,
            "user_answers": req.user_answers,
            "mode": "quiz_submit",
            "request_id": str(uuid.uuid4())
        }

        result = await app.ainvoke(state)

        if not result:
            raise ValueError("Evaluation failed")

        return {
            "score": result.get("score"),
            "feedback": result.get("feedback"),
            "weak_topic": result.get("weak_topic"),
            "explanation": result.get("explanation")  # tutor output
        }

    except Exception as e:
        logging.error(f"🔥 Error in /submit: {str(e)}")
        raise CustomException(e, sys)


# -------------------------
# Global Exception Handler
# -------------------------
@app_api.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    logging.error(f"🚨 CustomException: {exc}")

    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )


# -------------------------
# Root Health Check
# -------------------------
@app_api.get("/")
def health():
    return {"status": "running"}


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    logging.info("🚀 Starting FastAPI server...")
    uvicorn.run(app_api, host="0.0.0.0", port=8000)