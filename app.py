import streamlit as st
import random

# --- PAGE CONFIGURATION & BEAR THEME ---
st.set_page_config(page_title="Beary Good Phil 4 Study Game", page_icon="🐻", layout="centered")

# Custom CSS for a cute Bear / Forest Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f1ea;
        color: #3e2723;
    }
    h1 {
        color: #5d4037;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
    }
    .question-box {
        background-color: #e7cda2;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #8d6e63;
        margin-bottom: 20px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #795548;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #5d4037;
        color: #ffb300;
    }
    .explanation-box {
        background-color: #c8e6c9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin-top: 15px;
    }
    .wrong-box {
        background-color: #ffcdd2;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #c62828;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐻 Beary Good Phil 4 Study Game 🐾")
st.markdown("*Test your knowledge on Thomson, Marquis, Pogge, and Clinical Trials!*")

# --- QUESTION BANK ---
# You can add as many questions as you want here by copying the format!
questions = [
    {
        "question": "In the VIP Honda Civic case, a gang of car thieves leaves your car open and running, and the other Honda Civic owner mistakenly takes your car. What does this case provide a counterexample to?",
        "options": [
            "The Direct Killing Argument",
            "Exception to Moral Freedom",
            "Rights generators #1, #2, and #3 from Handout #3.3",
            "The Moderate Pro-Life View"
        ],
        "answer": "Rights generators #1, #2, and #3 from Handout #3.3",
        "explanation": "According to Handout 3.3 and your Practice Test #2, this specific case is meant to be a compelling candidate counterexample to the first three rights generation principles."
    },
    {
        "question": "According to your handout on Surfaxin, what is the 'Therapeutic Misconception'?",
        "options": [
            "The belief that placebos actually cure diseases.",
            "Confusing the main goal of a researcher (getting info) with the main goal of a doctor (preserving patient health).",
            "The belief that clinical trials are always morally permissible.",
            "The assumption that active-rich trials are always better than placebo-poor trials."
        ],
        "answer": "Confusing the main goal of a researcher (getting info) with the main goal of a doctor (preserving patient health).",
        "explanation": "Handout #2.0 explicitly defines the therapeutic misconception as the failure to separate a doctor's goal (patient health) from a researcher's goal (getting information)."
    },
    {
        "question": "Which of the following correctly identifies D-Labs' self-interested preferences regarding which type of trial to run (from best for them to worst)?",
        "options": [
            "placebo-rich > active-rich > placebo-poor > active-poor",
            "active-rich > active-poor > placebo-rich > placebo-poor",
            "placebo-poor > active-poor > placebo-rich > active-rich",
            "active-poor > placebo-poor > active-rich > placebo-rich"
        ],
        "answer": "placebo-rich > active-rich > placebo-poor > active-poor",
        "explanation": "Companies generally prefer placebo trials because they require smaller sample sizes and are cheaper/faster to run. 'Rich' countries are preferred if they can afford the drugs later."
    },
    {
        "question": "According to Thomson, what does the 'Extreme View' (EV) on abortion claim?",
        "options": [
            "Abortion is impermissible except to save the mother's life.",
            "Abortion is always impermissible, even to save the mother's life.",
            "Abortion is impermissible unless the mother performs it herself.",
            "Abortion is always permissible."
        ],
        "answer": "Abortion is always impermissible, even to save the mother's life.",
        "explanation": "Handout #3.2 defines the Extreme View (EV) as 'Abortion is always impermissible.' It does not even make exceptions for the life of the mother."
    },
    {
        "question": "In Thomson's arguments, how does the 'Slightly Less Extreme View' (SLEV) differ from the Moderate View (Mod-pro)?",
        "options": [
            "SLEV allows doctors to perform the abortion, Mod-pro does not.",
            "SLEV says only the mother herself can perform the emergency abortion to save her life; third parties (doctors) cannot.",
            "SLEV allows abortion for rape, Mod-pro does not.",
            "SLEV is Marquis's view, Mod-pro is Thomson's."
        ],
        "answer": "SLEV says only the mother herself can perform the emergency abortion to save her life; third parties (doctors) cannot.",
        "explanation": "Handout #3.2 notes that under SLEV, a woman may perform an abortion on herself to save her life, but a doctor (a third party) may not. The Moderate view allows the doctor to intervene."
    },
    {
        "question": "What is the main point of Thomson's Basic Violinist Case?",
        "options": [
            "To prove that fetuses are not persons.",
            "To show that the right to life does NOT include the right to be given the bare minimum one needs for continued life (like use of another's body).",
            "To prove the Direct Killing Argument is flawlessly logical.",
            "To argue for Pogge's Exception to Moral Freedom."
        ],
        "answer": "To show that the right to life does NOT include the right to be given the bare minimum one needs for continued life (like use of another's body).",
        "explanation": "Even if the violinist has a right to life, that right doesn't entitle him to use your kidneys for nine months. Thomson uses this to argue that a fetus's right to life doesn't automatically grant it the right to use the mother's body."
    },
    {
        "question": "What is the core premise of Don Marquis's argument against abortion?",
        "options": [
            "Abortion is a violation of the mother's bodily autonomy.",
            "Abortion is wrong because it deprives the fetus of a valuable future ('a future like ours').",
            "Abortion is wrong solely based on religious dogma.",
            "Abortion is wrong because fetuses feel pain."
        ],
        "answer": "Abortion is wrong because it deprives the fetus of a valuable future ('a future like ours').",
        "explanation": "Marquis argues that the primary reason killing adult humans is wrong is that it deprives them of a valuable future. He extends this to fetuses, claiming they also possess a 'future like ours'."
    },
    {
        "question": "According to the 'Direct Killing Argument' (DKA) presented in Handout 3.1, why might a doctor refuse an emergency abortion?",
        "options": [
            "Because letting the mother die is passive, whereas abortion involves directly killing an innocent person.",
            "Because the mother doesn't morally own her body.",
            "Because of the therapeutic misconception.",
            "Because the fetus has explicitly requested to use the body."
        ],
        "answer": "Because letting the mother die is passive, whereas abortion involves directly killing an innocent person.",
        "explanation": "Premise 6.4 of the DKA states that if one's only options are directly killing an innocent person or letting a person die, one must prefer letting the person die. Thomson attacks this."
    },
    {
        "question": "In the roommate case (Handout #1.0), what is the primary philosophical distinction being highlighted?",
        "options": [
            "Ontological Moral Skepticism vs. Epistemic Moral Realism",
            "Moral considerations (reasons) vs. all-things-considered conclusive moral norms (wrong/impermissible).",
            "The rights of the roommate vs. the rights of the landlord.",
            "Active-poor vs. placebo-poor scenarios."
        ],
        "answer": "Moral considerations (reasons) vs. all-things-considered conclusive moral norms (wrong/impermissible).",
        "explanation": "The handout explicitly uses the roommate locking you in the bathroom to distinguish between individual moral reasons that weigh on an action, versus the final, all-things-considered verdict of whether it was wrong."
    },
    {
        "question": "According to Pogge (Handout 2.2), what is 'Peter Singer’s famous argument' compared against?",
        "options": [
            "Thomson's Violinist",
            "Pogge's proposal, which is much narrower in application than Singer's broad principle to prevent bad things.",
            "Marquis's Future Like Ours",
            "The Havrix Trial guidelines"
        ],
        "answer": "Pogge's proposal, which is much narrower in application than Singer's broad principle to prevent bad things.",
        "explanation": "Singer argues that if we can prevent something bad without sacrificing anything nearly as important, we are obligated to do so. Pogge's requirement for drug companies is much narrower and specific to their institutional roles."
    }
]

# --- GAME LOGIC & SESSION STATE ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None
    # Shuffle options for the first question
    random.shuffle(questions[0]['options'])

def next_question():
    st.session_state.current_q += 1
    st.session_state.answered = False
    st.session_state.selected_option = None
    if st.session_state.current_q < len(questions):
        random.shuffle(questions[st.session_state.current_q]['options'])

def check_answer(option):
    st.session_state.selected_option = option
    st.session_state.answered = True
    if option == questions[st.session_state.current_q]['answer']:
        st.session_state.score += 1

# --- UI DISPLAY ---
st.sidebar.title("🐾 Bear Tracker")
st.sidebar.write(f"**Score:** {st.session_state.score} / {len(questions)}")
st.sidebar.write(f"**Progress:** Question {st.session_state.current_q + 1} of {len(questions)}")
st.sidebar.markdown("---")
st.sidebar.markdown("Keep going! You're going to crush Exam 2 tomorrow. 🐻💪")

if st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]
    
    st.markdown(f"<div class='question-box'>Q{st.session_state.current_q + 1}: {q['question']}</div>", unsafe_allow_html=True)
    
    if not st.session_state.answered:
        for option in q['options']:
            if st.button(option):
                check_answer(option)
                st.rerun()
    else:
        # Show what they selected
        st.write(f"You selected: **{st.session_state.selected_option}**")
        
        if st.session_state.selected_option == q['answer']:
            st.markdown("<div class='explanation-box'>🎉 <strong>Correct! Beary good job!</strong><br><br>" + q['explanation'] + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='wrong-box'>🐻 <strong>Oh no, that's not quite right.</strong><br><br><strong>Correct Answer:</strong> " + q['answer'] + "<br><br><strong>Why?</strong> " + q['explanation'] + "</div>", unsafe_allow_html=True)
        
        st.write("---")
        if st.button("Next Question 🐾"):
            next_question()
            st.rerun()

else:
    st.success("🎉 You finished the game!")
    st.balloons()
    st.markdown(f"### Final Score: {st.session_state.score} / {len(questions)}")
    st.markdown("You are officially prepared to tackle Prof. McHose's exam. Go get some sleep!")
    if st.button("Restart Game 🐻"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()
