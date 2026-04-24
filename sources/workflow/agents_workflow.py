from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from sources.logger import logging
from sources.exception import CustomException
import sys

# graph/state.py

from typing import TypedDict, List, Dict

class LearningState(TypedDict, total=False):
    input: str
    intent: str
    subject: str
    num_questions: int

    level: str
    weak_topic: str
    scores: Dict

    topics: List[str]
    quiz: str
    quiz_attempts: List[Dict]

    explanation: str
    feedback: str
    next_topic: str

# import agents
from sources.agents.intent_agent import intent_agent
from sources.agents.gap_agent import gap_agent
from sources.agents.planner_agent import planner_agent
from sources.agents.tutor_agent import tutor_agent
from sources.agents.assessment_agent import assessment_agent
from sources.agents.analytics_agent import analytics_agent

# create graph
graph = StateGraph(LearningState)

# add nodes
graph.add_node("intent", intent_agent)
graph.add_node("gap", gap_agent)
graph.add_node("planner", planner_agent)
graph.add_node("tutor", tutor_agent)
graph.add_node("assessment", assessment_agent)
graph.add_node("analytics", analytics_agent)

# entry point
graph.set_entry_point("intent")   

# route after intent which helps us to understand the intention of the user and route to the appropriate agent.
def route_after_intent(state):
    if state["intent"] == "quiz":
        return "gap"
    elif state["intent"] == "learn":
        return "planner"
    else:
        return "gap"

# after intent
graph.add_conditional_edges(
    "intent",
    route_after_intent,
    {
        "gap": "gap",
        "planner": "planner"
    }
)

# main flow
graph.add_edge("gap", "planner")
graph.add_edge("planner", "tutor")
graph.add_edge("tutor", "assessment")

# route after assessment which helps us to understand the number of attempts and route to the appropriate agent.
def route_after_assessment(state):
    # if no attempts yet → stop here
    if not state.get("quiz_attempts"):
        return END
    return "analytics"


graph.add_conditional_edges(
    "assessment",
    route_after_assessment,
    {
        "analytics": "analytics",
        END: END
    }
)

app = graph.compile()
