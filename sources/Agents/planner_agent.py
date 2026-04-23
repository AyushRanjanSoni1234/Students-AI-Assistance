from sources.model.model import LLM_Model
import json
from sources.logger import logging
from sources.exception import CustomException
import sys


llm = LLM_Model()

logging.info("Planner agent initialized successfully")

def planner_agent(state):
    try:
        logging.info("Planner agent called")
        subject = state["subject"]
        weak_topic = state.get("weak_topic", "")
        level = state.get("level", "beginner")

        prompt = f"""
        You are an AI curriculum planner.

        Subject: {subject}
        Student Level: {level}
        Weak Topic: {weak_topic}

        Generate a structured learning path:
        - 3 to 5 topics
        - Start from basics → advanced
        - Focus more on weak topic

        Return JSON:
        {{
        "topics": ["topic1", "topic2", "topic3"]
        }}
        """

        response = llm.generate_response(prompt).content

        try:
            parsed = json.loads(response)
            topics = parsed["topics"]
        except:
            topics = [weak_topic or f"{subject} basics"]

        logging.info("Planner agent completed successfully")
        return {"topics": topics}

    except Exception as e:
        logging.error("Error in planner agent")
        raise CustomException(e, sys)