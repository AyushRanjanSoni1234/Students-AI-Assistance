from sources.logger import logging
from sources.exception import CustomException
from sources.utils import calculate_score, get_weak_topics
import sys

logging.info("Analytics agent initialized successfully")

def analytics_agent(state):
    try:
        attempts = state.get("quiz_attempts", [])

        score = calculate_score(attempts)
        weak_topics = get_weak_topics(attempts)

        feedback = f"""
        Score: {score:.2f}%

        Weak Topics: {weak_topics if weak_topics else "None"}

        Next Step:
        - Revise weak topics
        - Practice again
        """

        return {
            **state,
            "score": score,
            "feedback": feedback,
            "weak_topic": weak_topics[0] if weak_topics else "None"
        }

        logging.info("Analytics agent completed successfully")

    except Exception as e:
        logging.error("Error in analytics agent")
        raise CustomException(e, sys)