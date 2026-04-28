from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
from sources.logger import logging

# -------------------------
# State Definition
# -------------------------
class LearningState(TypedDict, total=False):
    input: str
    intent: str
    mode: str   # "learn" | "quiz_generate" | "quiz_submit"

    subject: str
    topics: List[str]

    quiz: List[Dict]
    user_answers: List[str]

    score: float
    weak_topic: str
    feedback: str
    explanation: str


# -------------------------
# Import Agents
# -------------------------
from sources.agents.intent_agent import intent_agent
from sources.agents.planner_agent import planner_agent
from sources.agents.tutor_agent import tutor_agent
from sources.agents.quiz_agent import quiz_agent
from sources.agents.assessment_agent import assessment_agent
from sources.agents.analytics_agent import analytics_agent
from sources.agents.gap_agent import gap_agent

logging.info("Agents workflow created successfully")

# -------------------------
# Graph
# -------------------------
graph = StateGraph(LearningState)

# Nodes
graph.add_node("intent", intent_agent)
graph.add_node("planner", planner_agent)
graph.add_node("tutor", tutor_agent)
graph.add_node("quiz", quiz_agent)
graph.add_node("assessment", assessment_agent)
graph.add_node("analytics", analytics_agent)
graph.add_node("gap", gap_agent)

# Entry
graph.set_entry_point("intent")

# -------------------------
# Routing After Intent
# -------------------------
def route_after_intent(state):
    mode = state.get("mode", "learn")

    if mode == "learn":
        return "planner"

    elif mode == "quiz_generate":
        return "quiz"

    elif mode == "quiz_submit":
        return "assessment"

    return END


graph.add_conditional_edges(
    "intent",
    route_after_intent,
    {
        "planner": "planner",
        "quiz": "quiz",
        "assessment": "assessment",
        END: END
    }
)

# -------------------------
# ✅ Learn Flow
# -------------------------
graph.add_edge("planner", "tutor")
graph.add_edge("tutor", END)

# -------------------------
# ✅ Quiz Generation Flow
# -------------------------
graph.add_edge("quiz", END)

# -------------------------
# ✅ Quiz Submission Flow (FIXED)
# -------------------------
graph.add_edge("assessment", "analytics")
graph.add_edge("analytics", "gap")

# 🔥 FIX: go directly to tutor (NO planner)
graph.add_edge("gap", "tutor")

# tutor → END already defined above

# -------------------------
# Compile
# -------------------------
app = graph.compile()

logging.info("Agents workflow compiled successfully")