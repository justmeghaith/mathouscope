import random
import streamlit as st

# Set up the page title and icon
st.set_page_config(page_title="Random Math Quizzer", page_icon="🧮")


# --- QUESTION GENERATORS ---
def get_primary_question():
    """Generates simple arithmetic: addition, subtraction, multiplication."""
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        ans = num1 + num2
    elif operation == "-":
        # Keep it positive for primary school
        num1, num2 = max(num1, num2), min(num1, num2)
        ans = num1 - num2
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 12)
        ans = num1 * num2

    question = f"What is {num1} {operation} {num2}?"
    return question, str(ans)


def get_secondary_question():
    """Generates pre-algebra and algebra questions."""
    q_type = random.choice(["solve_x", "exponent", "percentage"])

    if q_type == "solve_x":
        # x + a = b
        a = random.randint(1, 15)
        ans = random.randint(1, 15)
        b = ans + a
        question = f"Solve for x:  x + {a} = {b}"
    elif q_type == "exponent":
        base = random.randint(2, 5)
        power = random.randint(2, 3)
        ans = base**power
        question = f"What is {base} to the power of {power}? (e.g., {base}^{power})"
    else:
        percent = random.choice([10, 20, 25, 50])
        total = random.randint(1, 10) * 20
        ans = int((percent / 100) * total)
        question = f"What is {percent}% of {total}?"

    return question, str(ans)


def get_college_question():
    """Generates introductory calculus, linear algebra, and log questions."""
    q_type = random.choice(["derivative", "logarithm", "matrix_det"])

    if q_type == "derivative":
        power = random.randint(3, 6)
        question = f"Find the derivative of f(x) = x^{power}. Enter just the power rule result (e.g., {power}x^{power-1})"
        ans = f"{power}x^{power-1}"
    elif q_type == "logarithm":
        base = random.choice([2, 10])
        ans = random.randint(2, 4)
        val = base**ans
        question = f"Evaluate: log_base_{base}({val})"
    else:
        # Simple 2x2 determinant
        a, b, c, d = (
            random.randint(1, 5),
            random.randint(1, 5),
            random.randint(1, 5),
            random.randint(1, 5),
        )
        ans = (a * d) - (b * c)
        question = f"Find the determinant of the 2x2 matrix: [[{a}, {b}], [{c}, {d}]]"

    return question, str(ans).strip()


# --- APP STATE MANAGEMENT ---
# Initialize session state variables so the app remembers them across clicks
if "current_question" not in st.state:
    st.state.current_question = None
    st.state.current_answer = None
    st.state.feedback = ""
    st.state.last_level = None

# --- UI DESIGN ---
st.title("🧮 Random Math Question Generator")
st.write("Test your skills across different education levels!")

# Sidebar for level selection
level = st.sidebar.radio(
    "Choose your level:", ["Primary School", "Secondary School", "College"]
)

# If the user switches levels, force a new question immediately
if level != st.state.last_level:
    st.state.last_level = level
    st.state.current_question = None
    st.state.feedback = ""

# Button to generate a new question
if st.button("Generate New Question") or st.state.current_question is None:
    if level == "Primary School":
        q, a = get_primary_question()
    elif level == "Secondary School":
        q, a = get_secondary_question()
    else:
        q, a = get_college_question()

    st.state.current_question = q
    st.state.current_answer = a
    st.state.feedback = ""  # Clear old feedback
    st.rerun()

# Display the question
st.markdown("---")
st.subheader("Question:")
st.info(st.state.current_question)

# Answer submission form
with st.form(key="answer_form", clear_on_submit=True):
    user_answer = st.text_input("Your Answer:").strip()
    submit_button = st.form_submit_button(label="Submit Answer")

    if submit_button:
        if user_answer.lower() == st.state.current_answer.lower():
            st.state.feedback = "✅ **Correct! Excellent job!**"
        else:
            st.state.feedback = (
                f"❌ **Incorrect.** The correct answer was: `{st.state.current_answer}`"
            )

# Show feedback below the form if it exists
if st.state.feedback:
    st.write(st.state.feedback)
