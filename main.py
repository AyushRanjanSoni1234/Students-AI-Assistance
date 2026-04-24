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
# Initialize Session State
# -------------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "input" not in st.session_state:
    st.session_state.input = ""

# -------------------------
# Step 1: User Input
# -------------------------
st.subheader("🎯 What do you want to learn?")

user_input = st.text_input(
    "Enter your request",
    placeholder="e.g. Create a quiz for Python with 10 questions"
)

# -------------------------
# Generate Quiz
# -------------------------
if st.button("Generate Quiz"):
    if not user_input:
        st.warning("Please enter something!")
    else:
        with st.spinner("Generating quiz..."):
            try:
                res = requests.post(
                    f"{API_URL}/generate",
                    json={"input": user_input}
                )

                data = res.json()

                # -------------------------
                # Fix: Ensure quiz is list
                # -------------------------
                quiz_data = data.get("quiz", [])

                if isinstance(quiz_data, str):
                    try:
                        quiz_data = json.loads(quiz_data)
                    except:
                        quiz_data = []

                st.session_state.quiz = quiz_data
                st.session_state.input = user_input

            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------
# Step 2: Show Quiz
# -------------------------
if st.session_state.quiz:

    # Show user input
    st.markdown("### 📝 Your Request")
    st.info(st.session_state.input)

    st.subheader("📘 Quiz")

    answers = []

    for i, q in enumerate(st.session_state.quiz):

        # -------------------------
        # Safety Check
        # -------------------------
        if not isinstance(q, dict):
            st.error("Invalid quiz format")
            continue

        st.markdown(f"**Q{i+1}. {q.get('question', '')}**")

        options = q.get("options", [])

        if options:
            ans = st.radio(
                "Choose your answer:",
                options,
                key=f"q_{i}"
            )
            answers.append(ans)
        else:
            st.error("No options available")

# -------------------------
# Step 3: Submit Quiz
# -------------------------
    if st.button("Submit Quiz"):

        # Check all answered
        if len(answers) != len(st.session_state.quiz):
            st.warning("Please answer all questions!")
        else:
            with st.spinner("Evaluating your answers..."):

                attempts = []

                for i, q in enumerate(st.session_state.quiz):
                    attempts.append({
                        "topic": q.get("topic", "general"),
                        "correct": answers[i] == q.get("answer")
                    })

                try:
                    res = requests.post(
                        f"{API_URL}/submit",
                        json={
                            "input": st.session_state.input,
                            "quiz_attempts": attempts
                        }
                    )

                    result = res.json()

                    # -------------------------
                    # Show Results
                    # -------------------------
                    st.subheader("📊 Results")

                    score = result.get("score", 0)

                    try:
                        score = float(score)
                        st.success(f"Score: {score:.2f}%")
                    except:
                        st.warning("Score not available")

                    st.markdown("### 📝 Feedback")
                    st.write(result.get("feedback", ""))

                    st.markdown("### ⚠️ Weak Topic")
                    st.write(result.get("weak_topic", ""))

                    st.markdown("### 📚 Explanation")
                    st.write(result.get("explanation", ""))

                except Exception as e:
                    st.error(f"Error: {e}")