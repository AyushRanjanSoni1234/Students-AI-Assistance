from sources.logger import logging
from sources.exception import CustomException
import sys

logging.info("Gap agent initialized successfully")

def gap_agent(state):
    try:
        logging.info("Gap agent called")
        attempts = state.get("quiz_attempts", [])

        if not attempts:
            return {
                "weak_topic": f"{state['subject']} basics",
                "level": "beginner"
            }

        topic_scores = {}

        for a in attempts:
            topic = a["topic"]
            correct = a["correct"]

            topic_scores.setdefault(topic, []).append(1 if correct else 0)

        avg_scores = {
            t: sum(v) / len(v) * 100
            for t, v in topic_scores.items()
        }

        weak_topic = min(avg_scores, key=avg_scores.get)

        logging.info("Gap agent completed successfully")
        return {
            "weak_topic": weak_topic,
            "scores": avg_scores
        }

    except Exception as e:
        logging.error("Error in gap agent")
        raise CustomException(e, sys)