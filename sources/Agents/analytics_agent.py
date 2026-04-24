from sources.logger import logging
from sources.exception import CustomException
from sources.utils import calculate_score, get_weak_topics
import sys

logging.info("Analytics agent initialized successfully")


def analytics_agent(state):
    try:
        logging.info("Analytics agent called")

        # -------------------------
        # Safe access
        # -------------------------
        attempts = state.get("quiz_attempts", [])

        # -------------------------
        # Calculate score
        # -------------------------
        score = calculate_score(attempts)

        # -------------------------
        # Get weak topics
        # -------------------------
        weak_topics = get_weak_topics(attempts)

        # -------------------------
        # Feedback
        # -------------------------
        feedback = f"""
        Your Score: {score:.2f}%

        Strengths:
        - Good understanding of correct answers

        Weak Areas:
        - {list(set(weak_topics)) if weak_topics else "None"}

        Recommendation:
        Practice weak topics and retry quiz.
        """

        logging.info("Analytics agent completed successfully")

        return {
            "score": score,
            "feedback": feedback,
            "weak_topic": weak_topics[0] if weak_topics else "None"
        }

    except Exception as e:
        logging.error("Error in analytics agent")
        raise CustomException(e, sys)