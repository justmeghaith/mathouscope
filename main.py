import random
import streamlit as st

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Math Scholar Tycoon", page_icon="🎓", layout="centered")

# --- AVATAR CATALOG ---
# A library of unlockable avatars using standard emojis
AVATAR_SHOP = {
    "Default Rookie": {"icon": "👶", "price": 0},
    "Math Cadet": {"icon": "🎒", "price": 15},
    "Algebra Knight": {"icon": "⚔️", "price": 40},
    "Geometry Wizard": {"icon": "🧙‍♂️", "price": 75},
    "Calculus Overlord": {"icon": "👑", "price": 150},
    "Cyber Einstein": {"icon": "🤖", "price": 300}
}

# --- STATE INITIALIZATION ---
if "coins" not in st.session_state:
    st.session_state.coins = 0
    st.session_state.questions_solved = 0
    st.session_state.current_avatar = "Default Rookie"
    st.session_state.unlocked_avatars = ["Default Rookie"]
    
    # Question specific states
    st.session_state.num1 = 0
    st.session_state.num2 = 0
    st.session_state.operator = "+"
    st.session_state.correct_answer = 0
    st.session_state.question_text = ""
    st.session_state.need_new_question = True
    st.session_state.feedback = ""

# --- QUESTION GENERATOR ENGINE ---
def generate_math_question(difficulty):
    if difficulty == "Primary School":
        # Simple arithmetic
        op = random.choice(["+", "-", "×"])
        if op == "+":
            n1, n2 = random.randint(1, 50), random.randint(1, 50)
            ans = n1 + n2
        elif op == "-":
            n1 = random.randint(20, 100)
            n2 = random.randint(1, n1)  # Keep positive results
            ans = n1 - n2
        else:
            n1, n2 = random.randint(2, 12), random.randint(1, 10)
            ans = n1 * n2
        q_text = f"What is {n1} {op} {n2}?"
        reward = 5

    elif difficulty == "Secondary School":
        # Basic algebra, exponents, and simple equations
        type_choice = random.choice(["solve_x", "exponent", "remainder"])
        if type_choice == "solve_x":
            # x + a = b
            a = random.randint(5, 30)
            ans = random.randint(5, 30)
            b = ans + a
            q_text = f"Solve for x:  x + {a} = {b}"
        elif type_choice == "exponent":
            n1 = random.randint(2, 12)
            q_text = f"What is {n1} squared ($ {n1}^2 $)?"
            ans = n1 ** 2
        else:
            n1 = random.randint(20, 100)
            q_text = f"What is the remainder when {n1} is divided by 6?"
            ans = n1 % 6
        reward = 15

    else:  # College
        # Logarithms, Matrices, Derivatives, and Sequences
        type_choice = random.choice(["derivative", "logarithm", "matrix"])
        if type_choice == "derivative":
            power = random.randint(3, 6)
            q_text = f"Find the slope (derivative) of $ f(x) = x^{power} $ at $ x = 1 $."
            ans = power # derivative is power * x^(power-1), at x=1 it is just power
        elif type_choice == "logarithm":
            base = random.choice([2, 3, 5])
            ans = random.randint(2, 4)
            val = base ** ans
            q_text = f"What is the value of $ \log_{base}({val}) $?"
        else:
            # Determinant of 2x2 matrix [[a, b], [c, d]]
            a, b, c, d = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
            q_text = f"Find the determinant of the 2x2 matrix: $ \\begin{{matrix}} {a} & {b} \\\\ {c} & {d} \\end{{matrix}} $"
            ans = (a * d) - (b * c)
        reward = 40

    st.session_state.question_text = q_text
    st.session_state.correct_answer = ans
    st.session_state.reward_value = reward
    st.session_state.need_new_question = False

# --- HEADER & ACCOUNTS ---
st.title("🎓 Math Scholar Tycoon")
st.write("Solve mathematical equations to earn coins and upgrade your profile avatar!")
st.markdown("---")

# Left Column: Profile & Shop | Right Column: Active Testing Center
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("👤 Your Profile")
    current_icon = AVATAR_SHOP[st.session_state.current_avatar]["icon"]
    
    # Custom CSS badge for avatar view box
    st.markdown(
        f"<div style='font-size: 72px; text-align: center; background: #262730; border-radius: 15px; padding: 10px;'>{current_icon}</div>", 
        unsafe_allow_html=True
    )
    st.write(f"**Title Rank:** {st.session_state.current_avatar}")
    
    # Stats HUD counters
    st.metric(label="Coin Bank", value=f"🪙 {st.session_state.coins}")
    st.metric(label="Solves Completed", value=f"✅ {st.session_state.questions_solved}")
    
    st.markdown("---")
    st.subheader("🛒 Avatar Shop")
    
    # Display catalog items
    for name, item in AVATAR_SHOP.items():
        if name in st.session_state.unlocked_avatars:
            if name == st.session_state.current_avatar:
                st.button(f"{item['icon']} {name} (Equipped)", key=f"shop_{name}", disabled=True, use_container_width=True)
            else:
                if st.button(f"Equip {item['icon']} {name}", key=f"shop_{name}", use_container_width=True):
                    st.session_state.current_avatar = name
                    st.rerun()
        else:
            btn_label = f"{item['icon']} {name} — 🪙 {item['price']}"
            if st.button(btn_label, key=f"shop_{name}", use_container_width=True):
                if st.session_state.coins >= item['price']:
                    st.session_state.coins -= item['price']
                    st.session_state.unlocked_avatars.append(name)
                    st.session_state.current_avatar = name
                    st.toast(f"Unlocked {name}!")
                    st.rerun()
                else:
                    st.error("Not enough coins!")

with col_right:
    st.subheader("📝 Testing Arena")
    
    # Stage select panel
    difficulty_tab = st.selectbox(
        "Choose Your Grade Level Level:",
        ["Primary School", "Secondary School", "College"]
    )
    
    # Generate question conditionally based on flag checks
    if st.session_state.need_new_question:
        generate_math_question(difficulty_tab)
        st.session_state.feedback = "" # reset feedback for new question
        
    st.markdown("#### Question:")
    st.info(st.session_state.question_text)
    st.caption(f"Potential Reward Bounty: 🪙 {st.session_state.reward_value} coins")
    
    # User Input fields
    user_ans = st.number_input("Type your answer below:", step=1, value=0, key="math_input_field")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Submit Answer", type="primary", use_container_width=True):
            if user_ans == st.session_state.correct_answer:
                st.session_state.feedback = "correct"
                st.session_state.coins += st.session_state.reward_value
                st.session_state.questions_solved += 1
                st.session_state.need_new_question = True
                st.rerun()
            else:
                st.session_state.feedback = "wrong"
    with c2:
        if st.button("Skip Question ⏭️", use_container_width=True):
            st.session_state.need_new_question = True
            st.rerun()
            
    # Display feedback message markers
    if st.session_state.feedback == "correct":
        st.success("🎉 Correct answer! Coins added to your bank.")
    elif st.session_state.feedback == "wrong":
        st.error("❌ Incorrect answer. Double-check your numbers and try again!")
