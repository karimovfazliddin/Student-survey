import streamlit as st
import json
from datetime import datetime

# ---------------- DATA ----------------
version_float = 1.0

questions = [
    {"q": "Feedback is viewed as an opportunity to improve performance.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Negative feedback makes it harder to stay motivated.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Feedback from teachers or supervisors is taken seriously.",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Significantly",3),("Extremely",4)]},

    {"q": "There is a tendency to reflect on feedback before making improvements.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Critical comments reduce confidence in abilities.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Feedback is actively used to improve future performance.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "It is easy to accept constructive criticism.",
     "opts": [("Very easy",0),("Easy",1),("Neutral",2),("Difficult",3),("Very difficult",4)]},

    {"q": "Motivation increases after receiving useful feedback.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Feedback is ignored when it feels too harsh.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Feedback helps identify personal weaknesses.",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Significantly",3),("Extremely",4)]},

    {"q": "There is a willingness to change behavior based on feedback.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Feedback is perceived as personal criticism rather than guidance.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Feedback encourages setting new goals.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Emotional reactions interfere with using feedback effectively.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "There is a belief that improvement is possible through effort.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]}
]

psych_states = {
    "Very High Growth Orientation": (0, 12),
    "Positive Feedback Engagement": (13, 24),
    "Moderate Feedback Sensitivity": (25, 36),
    "High Feedback Resistance": (37, 48),
    "Critical Feedback Avoidance State": (49, 60)
}

# ---------------- FUNCTIONS ----------------
def validate_name(name):
    return len(name.strip()) > 0 and all(c.isalpha() or c in "-' " for c in name)

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score):
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Feedback Survey", page_icon="📝")

st.title("📝 Feedback Reception & Improvement Motivation Survey")
st.write("Please fill in your details and answer all questions.")

# ---- User Info ----
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# ---- Start Survey ----
if st.button("Start Survey"):

    errors = []

    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must contain only digits.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("Inputs are valid. Please answer the questions below.")

        total_score = 0
        answers = []

        for i, q in enumerate(questions):
            option_labels = [opt[0] for opt in q["opts"]]
            selected = st.selectbox(f"Q{i+1}. {q['q']}", option_labels, key=i)

            score = next(score for text, score in q["opts"] if text == selected)
            total_score += score

            answers.append({
                "question": q["q"],
                "selected_option": selected,
                "score": score
            })

        result = interpret_score(total_score)

        st.markdown(f"## ✅ Result: {result}")
        st.markdown(f"**Total Score:** {total_score}")

        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": result,
            "answers": answers,
            "version": version_float
        }

        filename = f"{sid}_result.json"
        save_json(filename, record)

        st.success(f"Your results have been saved as {filename}")

        st.download_button(
            label="Download Results (JSON)",
            data=json.dumps(record, indent=2),
            file_name=filename,
            mime="application/json"
        )