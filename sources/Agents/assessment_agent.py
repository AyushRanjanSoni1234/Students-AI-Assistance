from sources.logger import logging
from sources.exception import CustomException
import sys

logging.info("Assessment agent initialized successfully")


def assessment_agent(state):
    try:
        quiz = state.get("quiz", [])
        user_answers = state.get("user_answers", [])

        attempts = []

        for q, user_ans in zip(quiz, user_answers):
            correct_ans = q.get("answer")

            correct = str(user_ans).strip().lower() == str(correct_ans).strip().lower()

            attempts.append({
                "question": q.get("question"),
                "topic": q.get("topic", "general"),
                "correct": correct
            })

        return {**state, "quiz_attempts": attempts}
        logging.info("Assessment agent completed successfully")

    except Exception as e:
        raise CustomException(e, sys)