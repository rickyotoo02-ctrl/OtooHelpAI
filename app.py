import streamlit as st
import ollama
import json
from pathlib import Path

st.set_page_config(
    page_title="AI Student Learning Assistant",
    page_icon="📚"
)

st.title("AI Student Learning Assistant")
st.caption("Your personal AI-powered study companion")
st.warning(
    "AI-generated content may contain inaccuracies. "
    "Always verify important information with reliable sources."
)
st.sidebar.title("Learning Settings")

st.sidebar.info(
    "Choose your learning mode and difficulty level "
    "to personalize your study experience."
)

# Permanent history storage
history_file = Path(__file__).parent / "history.json"

def save_history():
    history_file.write_text(
        json.dumps(st.session_state.history, indent=4),
        encoding="utf-8"
    )

if "history" not in st.session_state:
    if history_file.exists():
        st.session_state.history = json.loads(
            history_file.read_text(encoding="utf-8")
        )
    else:
        st.session_state.history = []

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_id" not in st.session_state:
    st.session_state.quiz_id = 0

# Learning settings
mode = st.sidebar.selectbox(
    "Choose a learning mode",
    ["Explain a concept", "Simplify a concept",
     "Generate study notes", "Generate a quiz"]
)

level = st.sidebar.selectbox(
    "Choose your difficulty level",
    ["Beginner", "Intermediate", "Advanced"]
)

user_input = st.text_area("Enter your topic or question")

# AI generation
if st.button("Generate"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            try:
                st.session_state.quiz = []

                if mode == "Generate a quiz":

                    prompt = f"""
                    Generate 5 multiple-choice questions.
                    Topic: {user_input}
                    Difficulty: {level}

                    Return a JSON object with a questions list.
                    Each question must contain:
                    question: the question text
                    options: a list of 4 answer choices
                    answer: the exact correct option
                    explanation: why the answer is correct
                    """

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        format="json"
                    )

                    data = json.loads(
                        response["message"]["content"]
                    )

                    questions = data["questions"]

                    if len(questions) != 5 or not all(
                        isinstance(q["question"], str)
                        and isinstance(q["options"], list)
                        and len(q["options"]) == 4
                        and all(
                            isinstance(option, str)
                            for option in q["options"]
                        )
                        and len(set(q["options"])) == 4
                        and q["answer"] in q["options"]
                        and isinstance(q["explanation"], str)
                        for q in questions
                    ):
                        raise ValueError("Invalid quiz format")

                    st.session_state.quiz = questions
                    st.session_state.quiz_id += 1

                else:
                    prompt = f"""
                    You are an educational AI assistant.
                    Task: {mode}
                    Difficulty: {level}
                    Topic: {user_input}

                    Provide a clear and accurate response.
                    Use examples when appropriate.
                    """

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    st.session_state.history.append({
                        "question": user_input,
                        "answer": response["message"]["content"],
                        "mode": mode,
                        "level": level
                    })

                    save_history()

            except Exception:
                st.error("Generation failed. Please try again.")
    else:
        st.warning("Please enter a topic.")

# Interactive quizzes
if mode == "Generate a quiz" and st.session_state.quiz:

    st.subheader("Practice Quiz")

    answers = []

    with st.form("quiz_form"):

        for i, q in enumerate(st.session_state.quiz):

            st.write(f"**Question {i + 1}: {q['question']}**")

            selected = st.radio(
                "Select your answer",
                q["options"],
                index=None,
                key=f"quiz_{st.session_state.quiz_id}_{i}"
            )

            answers.append(selected)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Please answer every question.")
        else:
            score = 0

            for i, q in enumerate(st.session_state.quiz):

                if answers[i] == q["answer"]:
                    score += 1
                    st.success(f"Question {i + 1}: Correct!")
                else:
                    st.error(
                        f"Question {i + 1}: Correct answer: "
                        f"{q['answer']}"
                    )

                st.write(q["explanation"])

            total = len(st.session_state.quiz)

            st.subheader(f"Your score: {score}/{total}")
            st.progress(score / total)

# Clear history
if st.button("Clear History"):
    st.session_state.history = []
    save_history()

# Learning Dashboard
st.divider()
st.subheader("Learning Dashboard")

history = st.session_state.history

col1, col2, col3 = st.columns(3)

col1.metric("Study Sessions", len(history))

col2.metric(
    "Study Notes",
    sum(item["mode"] == "Generate study notes"
        for item in history)
)

col3.metric(
    "Topics Studied",
    len(set(item["question"] for item in history))
)

# Learning History
st.divider()
st.subheader("Learning History")

if not history:
    st.info("Your study materials will appear here.")

for i, item in enumerate(reversed(history)):

    with st.expander(item["question"], expanded=True):

        st.caption(f'{item["mode"]} | {item["level"]}')
        st.markdown(item["answer"])

        st.download_button(
            label="Download Study Material",
            data=item["answer"],
            file_name="study_notes.txt",
            mime="text/plain",
            key=f"download_{i}"
        )