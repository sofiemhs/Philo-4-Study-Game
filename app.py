import streamlit as st
import re
import random

# --- PAGE CONFIGURATION & THEME ---
st.set_page_config(page_title="Phil 4 Master Study App", page_icon="🐻", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f1ea; color: #3e2723; }
    h1, h2, h3 { color: #5d4037; font-family: 'Courier New', Courier, monospace; }
    .story-box { background-color: #e7cda2; padding: 20px; border-radius: 15px; border: 2px solid #8d6e63; margin-bottom: 20px; font-size: 18px; }
    .vocab-box { background-color: #c8e6c9; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; margin-bottom: 15px; }
    .error-box { background-color: #ffcdd2; padding: 15px; border-radius: 10px; border-left: 5px solid #c62828; margin-bottom: 15px; }
    .flashcard { background-color: #ffffff; padding: 40px; border-radius: 15px; border: 3px dashed #8d6e63; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #795548; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #5d4037; color: #ffb300; }
    </style>
""", unsafe_allow_html=True)

# --- COURSE DATA (Strictly from Notes) ---
vocab_defs = {
    "Moral Considerations": "The individual factors that weigh for or against an action (a.k.a moral reasons).",
    "All-Things-Considered Moral Norms": "The final, conclusive verdict of whether an action is wrong or morally impermissible.",
    "Therapeutic Misconception": "When a participant confuses a researcher's main goal (to get information) with a doctor's main goal (patient health).",
    "Exception to Moral Freedom": "Pogge's principle: You cannot exploit desperate people for your own ends, even if you are providing a net benefit.",
    "Extreme View (EV)": "Abortion is always impermissible, even to save the mother's life.",
    "Slightly Less Extreme View (SLEV)": "Abortion is impermissible EXCEPT to save the mother's life AND the mother performs it herself (a doctor/third party may not).",
    "Moderate Pro-life View (Mod-pro)": "Abortion is impermissible EXCEPT to save the mother's life (a doctor may perform it).",
    "Right to Life (Thomson)": "Does NOT include the right to be given the bare minimum one needs for continued life (e.g., use of another's body).",
    "Counterexample": "A scenario used to disprove a principle (e.g., VIP Honda Civic disproves Rights Generators 1-3).",
    "A Future Like Ours (FLO)": "Marquis's argument that killing is wrong because it deprives the victim of a valuable future."
}

# Final Exam Data (From Practice Test #2.0)
exam_questions = [
    {
        "q": "According to Pogge, which of the following principles entails (or 'says') that it would have been wrong for D-Lab to run the clinical trial that they originally planned to run in Bolivia?",
        "options": ["(a) Moral Freedom", "(b) Moral Conditional", "(c) Moral Constraint", "(d) Exception to Moral Freedom", "(e) Moral Exploitation"],
        "ans": "(d) Exception to Moral Freedom"
    },
    {
        "q": "Pick the answer that correctly identifies D-Labs' self-interested preferences regarding which type of trial to run and where to run it. (Assume none are illegal).",
        "options": ["(a) placebo-rich > active-rich > placebo-poor > active-poor", "(b) placebo-poor > active-poor > placebo-rich > active-rich", "(c) active-poor > placebo-poor > active-rich > placebo-rich", "(d) active-rich > active-poor > placebo-rich > placebo-poor"],
        "ans": "(a) placebo-rich > active-rich > placebo-poor > active-poor"
    },
    {
        "q": "Pick the answer that correctly ranks the moral goodness of those possibilities.",
        "options": ["(a) placebo-rich > active-rich > placebo-poor > active-poor", "(b) active-rich > active-poor > placebo-rich > placebo-poor", "(c) placebo-poor > active-poor > placebo-rich > active-rich"],
        "ans": "(b) active-rich > active-poor > placebo-rich > placebo-poor"
    },
    {
        "q": "The VIP Honda Civic Case (where an innocent person accidentally drives off in your running car). Handout #3.3 presents three principles about rights generation. The case presented in this question provides a compelling counterexample to all three of those principles.",
        "options": ["(a) True", "(b) False"],
        "ans": "(a) True"
    }
]

# --- SESSION STATE ---
def init_state():
    defaults = {
        'stage': 0, 'sub_stage': 0, 'learned_vocab': [], 'struggled_queue': [],
        'failed_check': False, 'exam_score': 0, 'exam_q': 0, 'flashcards': list(vocab_defs.keys()),
        'fc_index': 0, 'fc_show_back': False, 'confirm_restart': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# Helpers
def next_stage(): st.session_state.stage += 1; st.session_state.sub_stage = 0; st.session_state.failed_check = False
def fail_check(): st.session_state.failed_check = True; st.session_state.sub_stage = 0
def pass_check(vocab_words):
    st.session_state.failed_check = False
    st.session_state.sub_stage += 1
    for w in vocab_words:
        if w not in st.session_state.learned_vocab:
            st.session_state.learned_vocab.append(w)
def add_struggle(topic):
    if topic not in st.session_state.struggled_queue:
        st.session_state.struggled_queue.append(topic)
def check_spelling(user_input, valid_phrases):
    clean_in = re.sub(r'[^\w\s]', '', user_input).lower().strip()
    return any(re.sub(r'[^\w\s]', '', p).lower().strip() in clean_in for p in valid_phrases)

# --- SIDEBAR ---
st.sidebar.title("🐾 Bear Tracker")
if st.sidebar.button("Restart Entire Journey 🔄"):
    st.session_state.confirm_restart = not st.session_state.confirm_restart
if st.session_state.confirm_restart:
    st.sidebar.warning("Are you sure? This deletes all progress.")
    if st.sidebar.button("YES, RESTART"):
        st.session_state.clear()
        init_state()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Known Vocab")
for word in st.session_state.learned_vocab:
    with st.sidebar.expander(f"✅ {word}"):
        st.write(vocab_defs[word])

# --- STAGE 0: Intro ---
if st.session_state.stage == 0:
    st.title("🐻 Phil 4 Master Study App")
    st.write("Welcome! If you fail a knowledge check, you must re-read the material. Struggles are tracked for a review quiz before the final exam. Let's begin!")
    if st.button("Start Journey"): next_stage(); st.rerun()

# --- STAGE 1: Skepticism ---
elif st.session_state.stage == 1:
    st.title("Chapter 1: Moral Skepticism (Handout 1.0)")
    
    if st.session_state.sub_stage == 0:
        if st.session_state.failed_check:
            st.markdown("<div class='error-box'>🐻 <b>You failed the check! Re-read carefully:</b><br>Prof. McHose strictly separates the *reasons* for an action (Moral Considerations) from the *final verdict* of an action (All-Things-Considered Moral Norms).</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='story-box'><b>Read:</b> Your roommate locks you in the bathroom so they can study and beat the curve. Almost everyone agrees this is wrong. McHose uses this to separate (i) <b>Moral Considerations</b> (the little weights/reasons for or against) from (ii) <b>All-Things-Considered Moral Norms</b> (the conclusive verdict that it is impermissible).</div>", unsafe_allow_html=True)
        
        st.write("<b>Knowledge Check:</b> Which term represents the 'conclusive' moral verdict?")
        if st.button("Moral Considerations"): add_struggle("Moral Considerations vs Norms"); fail_check(); st.rerun()
        if st.button("All-Things-Considered Moral Norms"): pass_check(["Moral Considerations", "All-Things-Considered Moral Norms"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.write("✏️ **Drill:** Type the specific term for the factors that weigh for/against an action (a.k.a 'moral reasons').")
        ans = st.text_input("Answer:")
        if ans:
            if check_spelling(ans, ["moral considerations"]):
                st.success("Perfect!")
                if st.button("Next Chapter"): next_stage(); st.rerun()
            else:
                st.error("Hint: Moral C__________s")
                add_struggle("Moral Considerations vs Norms")

# --- STAGE 2: Pogge & Clinical Trials ---
elif st.session_state.stage == 2:
    st.title("Chapter 2: The Surfaxin Trial & Pogge")
    
    if st.session_state.sub_stage == 0:
        if st.session_state.failed_check:
            st.markdown("<div class='error-box'>🐻 <b>Review:</b> The Therapeutic Misconception is about confusing the <b>researcher's goal (info)</b> with the <b>doctor's goal (health)</b>. The Exception to Moral Freedom is about <b>exploiting desperation</b>.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='story-box'><b>Read:</b> D-Lab runs a placebo-controlled trial on premature babies in Bolivia. <br><br>1. <b>Therapeutic Misconception:</b> Participants confuse a researcher's goal (getting data) with a doctor's goal (saving patients).<br>2. <b>Exception to Moral Freedom:</b> Pogge argues via the Eccentric Filmmaker that you cannot exploit desperate people, even if you give them a net benefit.</div>", unsafe_allow_html=True)
        
        st.write("<b>Knowledge Check:</b> Which principle says you cannot exploit desperate people even for a net benefit?")
        if st.button("Therapeutic Misconception"): add_struggle("Pogge's Principles"); fail_check(); st.rerun()
        if st.button("Exception to Moral Freedom"): pass_check(["Therapeutic Misconception", "Exception to Moral Freedom"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.write("✏️ **Drill:** What do we call it when a patient mistakes a researcher for a treating physician?")
        ans = st.text_input("Answer:")
        if ans:
            if check_spelling(ans, ["therapeutic misconception"]):
                st.success("Nailed it!")
                if st.button("Next Chapter"): next_stage(); st.rerun()
            else:
                st.error("Hint: T__________ M___________")
                add_struggle("Pogge's Principles")

# --- STAGE 3: Thomson ---
elif st.session_state.stage == 3:
    st.title("Chapter 3: Thomson & Abortion")
    
    if st.session_state.sub_stage == 0:
        if st.session_state.failed_check:
            st.markdown("<div class='error-box'>🐻 <b>Review:</b> The Extreme View (EV) allows NO exceptions. Slightly Less Extreme View (SLEV) allows the mother to abort to save her life, but NOT a doctor.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='story-box'><b>Read:</b> Thomson defines views strictly:<br>- <b>Extreme View (EV):</b> Abortion is always impermissible.<br>- <b>SLEV:</b> Impermissible except to save mother's life, AND the mother herself must perform it (third party/doctor cannot).<br><br>The Famous Violinist shows that the <b>Right to Life</b> does NOT include the right to the bare minimum needed for continued life (like someone else's body).</div>", unsafe_allow_html=True)
        
        st.write("<b>Knowledge Check:</b> Under SLEV, can a doctor perform an emergency abortion to save the mother?")
        if st.button("Yes"): add_struggle("Thomson's Views (EV/SLEV)"); fail_check(); st.rerun()
        if st.button("No, only the mother can"): pass_check(["Extreme View (EV)", "Slightly Less Extreme View (SLEV)", "Right to Life (Thomson)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.write("✏️ **Drill:** Type the 2-word phrase for the view that abortion is ALWAYS impermissible.")
        ans = st.text_input("Answer:")
        if ans:
            if check_spelling(ans, ["extreme view", "ev"]):
                st.success("Correct!")
                if st.button("Next Chapter"): next_stage(); st.rerun()
            else:
                st.error("Hint: E______ V___")
                add_struggle("Thomson's Views (EV/SLEV)")

# --- STAGE 4: Marquis ---
elif st.session_state.stage == 4:
    st.title("Chapter 4: Marquis")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Read:</b> Marquis avoids the 'personhood' debate. He argues killing is wrong simply because it deprives the victim of <b>A Future Like Ours (FLO)</b>. Since a fetus has a valuable future, killing it is wrong.</div>", unsafe_allow_html=True)
        st.write("<b>Knowledge Check:</b> Why is killing wrong according to Marquis?")
        if st.button("It directly kills an innocent person (DKA)"): add_struggle("Marquis FLO"); fail_check(); st.rerun()
        if st.button("It deprives them of a future like ours"): pass_check(["A Future Like Ours (FLO)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.write("✏️ **Drill:** What is the 4-word phrase (or 3-letter acronym) for Marquis's main argument?")
        ans = st.text_input("Answer:")
        if ans:
            if check_spelling(ans, ["future like ours", "flo"]):
                if st.button("Proceed to Smart Review"): next_stage(); st.rerun()
            else:
                st.error("Hint: F. L. O.")

# --- STAGE 5: Smart Review ---
elif st.session_state.stage == 5:
    st.title("🧠 Smart Review")
    if len(st.session_state.struggled_queue) == 0:
        st.success("Wow! You didn't struggle with any topics. You are ready for the Final Exam!")
        if st.button("Take Final Exam"): next_stage(); st.rerun()
    else:
        st.warning(f"Before the exam, you need to acknowledge the topics you missed: {', '.join(st.session_state.struggled_queue)}")
        st.write("Go review the sidebar definitions for these topics!")
        if st.button("I have reviewed them. Start Exam!"): next_stage(); st.rerun()

# --- STAGE 6: FINAL EXAM ---
elif st.session_state.stage == 6:
    st.title("📝 Practice Final Exam #2.0")
    st.write("Format matches Professor McHose's exam exactly.")
    
    q_data = exam_questions[st.session_state.exam_q]
    st.markdown(f"**Question {st.session_state.exam_q + 1} of {len(exam_questions)}**")
    st.write(q_data["q"])
    
    for opt in q_data["options"]:
        if st.button(opt):
            if opt == q_data["ans"]:
                st.session_state.exam_score += 1
            st.session_state.exam_q += 1
            st.rerun()
            
    if st.session_state.exam_q >= len(exam_questions):
        st.session_state.stage = 7 # Move to results
        st.rerun()

# --- STAGE 7: EXAM RESULTS ---
elif st.session_state.stage == 7:
    st.title("📊 Exam Results")
    score_pct = (st.session_state.exam_score / len(exam_questions)) * 100
    st.write(f"### You scored: {st.session_state.exam_score} / {len(exam_questions)} ({score_pct}%)")
    
    if score_pct >= 75:
        st.success("🎉 You passed the Final Exam! You have unlocked Flashcard Mode.")
        if st.button("Start Flashcards 🃏"): next_stage(); st.rerun()
    else:
        st.error("You need at least 75% to unlock Flashcards. Keep studying!")
        if st.button("Retake Exam"):
            st.session_state.exam_score = 0
            st.session_state.exam_q = 0
            st.session_state.stage = 6
            st.rerun()

# --- STAGE 8: FLASHCARDS ---
elif st.session_state.stage == 8:
    st.title("🃏 Mastery Flashcards")
    
    if len(st.session_state.flashcards) == 0:
        st.balloons()
        st.success("You have mastered every single card! You are 100% ready for the test tomorrow.")
        if st.button("Reset Deck"):
            st.session_state.flashcards = list(vocab_defs.keys())
            st.session_state.fc_index = 0
            st.session_state.fc_show_back = False
            st.rerun()
    else:
        # Prevent index out of bounds if deck shrinks
        if st.session_state.fc_index >= len(st.session_state.flashcards):
            st.session_state.fc_index = 0
            
        current_card = st.session_state.flashcards[st.session_state.fc_index]
        st.write(f"Cards remaining: {len(st.session_state.flashcards)}")
        
        if not st.session_state.fc_show_back:
            st.markdown(f"<div class='flashcard'>{current_card}</div>", unsafe_allow_html=True)
            if st.button("Show Answer"):
                st.session_state.fc_show_back = True
                st.rerun()
        else:
            st.markdown(f"<div class='flashcard' style='background-color:#e8f5e9;'><b>{current_card}</b><br><br><span style='font-size:18px; font-weight:normal;'>{vocab_defs[current_card]}</span></div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ I got it wrong"):
                    # Moves to next card, keeps this one in the deck to see again later
                    st.session_state.fc_index += 1
                    st.session_state.fc_show_back = False
                    st.rerun()
            with col2:
                if st.button("✅ I knew this"):
                    # Removes from deck
                    st.session_state.flashcards.pop(st.session_state.fc_index)
                    st.session_state.fc_show_back = False
                    st.rerun()
