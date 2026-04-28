import streamlit as st
import requests
import json

# -------------------------
# Config
# -------------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Students AI Assistance",
    layout="wide"
)

st.title("🧠 Students AI Assistance")

# -------------------------
# Session State
# -------------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "input" not in st.session_state:
    st.session_state.input = ""

if "answers" not in st.session_state:
    st.session_state.answers = []

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "explanation" not in st.session_state:
    st.session_state.explanation = None


# -------------------------
# User Input
# -------------------------
st.subheader("🎯 What do you want to learn?")

user_input = st.text_input(
    "Enter your request",
    placeholder="e.g. Learn Python basics OR Create quiz for Python"
)

col1, col2 = st.columns(2)

# -------------------------
# 🧠 LEARN BUTTON
# -------------------------
with col1:
    if st.button("🧠 Learn Topic"):

        # reset quiz
        st.session_state.quiz = None
        st.session_state.answers = []
        st.session_state.submitted = False

        if not user_input:
            st.warning("Please enter something!")
        else:
            with st.spinner("Generating explanation..."):
                try:
                    res = requests.post(
                        f"{API_URL}/generate",
                        json={
                            "input": user_input,
                            "mode": "learn"
                        },
                        timeout=30
                    )

                    if res.status_code != 200:
                        st.error("Server error")
                        st.stop()

                    data = res.json()

                    if "error" in data:
                        st.error(data["error"])
                        st.stop()

                    st.session_state.explanation = data.get("explanation")

                except Exception as e:
                    st.error(f"Error: {e}")


# -------------------------
# 📝 QUIZ BUTTON
# -------------------------
with col2:
    if st.button("📝 Generate Quiz"):

        st.session_state.explanation = None
        st.session_state.quiz = None
        st.session_state.answers = []
        st.session_state.submitted = False

        if not user_input:
            st.warning("Please enter something!")
        else:
            with st.spinner("Generating quiz..."):
                try:
                    res = requests.post(
                        f"{API_URL}/generate",
                        json={
                            "input": user_input,
                            "mode": "quiz_generate"
                        },
                        timeout=30
                    )

                    if res.status_code != 200:
                        st.error("Server error")
                        st.stop()

                    data = res.json()

                    if "error" in data:
                        st.error(data["error"])
                        st.stop()

                    quiz_data = data.get("quiz", [])

                    # handle string case
                    if isinstance(quiz_data, str):
                        try:
                            quiz_data = json.loads(quiz_data)
                        except:
                            quiz_data = []

                    if not quiz_data:
                        st.error("No quiz generated")
                    else:
                        st.session_state.quiz = quiz_data
                        st.session_state.input = user_input
                        st.session_state.answers = [None] * len(quiz_data)

                except Exception as e:
                    st.error(f"Error: {e}")


# -------------------------
# 🧠 SHOW EXPLANATION
# -------------------------
if st.session_state.explanation:
    st.subheader("📚 Explanation")
    st.write(st.session_state.explanation)


# -------------------------
# 📝 SHOW QUIZ
# -------------------------
if st.session_state.quiz:

    st.markdown("### 📝 Your Request")
    st.info(st.session_state.input)

    st.subheader("📘 Quiz")

    for i, q in enumerate(st.session_state.quiz):

        st.markdown(f"**Q{i+1}. {q.get('question', '')}**")

        options = q.get("options", [])

        selected = st.radio(
            "Choose your answer:",
            options,
            key=f"q_{i}"
        )

        st.session_state.answers[i] = selected


    # -------------------------
    # Submit Quiz
    # -------------------------
    if st.button("Submit Quiz"):

        if None in st.session_state.answers:
            st.warning("Please answer all questions!")
        else:
            with st.spinner("Evaluating..."):
                try:
                    res = requests.post(
                        f"{API_URL}/submit",
                        json={
                            "input": st.session_state.input,
                            "quiz": st.session_state.quiz,
                            "user_answers": st.session_state.answers
                        },
                        timeout=30
                    )

                    if res.status_code != 200:
                        st.error("Server error")
                        st.stop()

                    result = res.json()

                    if "error" in result:
                        st.error(result["error"])
                        st.stop()

                    st.session_state.submitted = True

                    # Results
                    st.subheader("📊 Results")

                    score = float(result.get("score", 0))
                    st.success(f"Score: {score:.2f}%")

                    st.markdown("### 📝 Feedback")
                    st.write(result.get("feedback"))

                    st.markdown("### ⚠️ Weak Topic")
                    st.write(result.get("weak_topic"))

                    st.markdown("### 📚 Explanation")
                    st.write(result.get("explanation"))

                except Exception as e:
                    st.error(f"Error: {e}")


# -------------------------
# Correct Answers
# -------------------------
if st.session_state.quiz and st.session_state.submitted:

    st.markdown("### ✅ Correct Answers")

    for i, q in enumerate(st.session_state.quiz):
        correct = q.get("answer")
        user_ans = st.session_state.answers[i]

        if user_ans == correct:
            st.success(f"Q{i+1}: Correct ✅")
        else:
            st.error(f"Q{i+1}: Wrong ❌ (Correct: {correct})")


# -------------------------
# Reset
# -------------------------
if st.button("🔄 Reset"):
    st.session_state.clear()