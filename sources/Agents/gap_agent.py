from sources.logger import logging
from sources.exception import CustomException
import sys

logging.info("Gap agent initialized successfully")

def gap_agent(state):
    try:
        logging.info("Gap agent called")

        attempts = state.get("quiz_attempts", [])
        subject = state.get("subject", "general")

        # -------------------------
        # No attempts → default
        # -------------------------
        if not attempts:
            return {
                "weak_topic": f"{subject} basics",
                "level": "beginner",
                "scores": {},
                "confidence": 0
            }

        topic_scores = {}

        # -------------------------
        # Safe processing
        # -------------------------
        for a in attempts:
            topic = a.get("topic", "unknown")
            correct = a.get("correct", False)

            # normalize correct value
            correct = bool(correct)

            topic_scores.setdefault(topic, []).append(1 if correct else 0)

        # -------------------------
        # Average score
        # -------------------------
        avg_scores = {
            t: (sum(v) / len(v)) * 100
            for t, v in topic_scores.items()
        }

        # -------------------------
        # Weak topic
        # -------------------------
        weak_topic = min(avg_scores, key=avg_scores.get)
        weak_score = avg_scores[weak_topic]

        # -------------------------
        # Level mapping
        # -------------------------
        if weak_score < 40:
            level = "beginner"
        elif weak_score < 70:
            level = "intermediate"
        else:
            level = "advanced"

        # -------------------------
        # Confidence (based on attempts)
        # -------------------------
        total_attempts = sum(len(v) for v in topic_scores.values())

        logging.info("Gap agent completed successfully")

        return {
            "weak_topic": weak_topic,
            "level": level,
            "scores": avg_scores,
            "confidence": total_attempts
        }

    except Exception as e:
        logging.error("Error in gap agent")
        raise CustomException(e, sys)