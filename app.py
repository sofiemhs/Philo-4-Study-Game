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
    .drill-box { background-color: #bbdefb; padding: 15px; border-radius: 10px; border-left: 5px solid #1976d2; margin-bottom: 15px; }
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

exam_questions = [
    {
        "q": "According to Pogge, which of the following principles entails (or 'says') that it would have been wrong for D-Lab to run the clinical trial that they originally planned to run in Bolivia?",
        "options": ["(a) Moral Freedom", "(b) Moral Conditional", "(c) Moral Constraint", "(d) Exception to Moral Freedom", "(e) Moral Exploitation"],
        "ans": "(d) Exception to Moral Freedom"
    },
    {
        "q": "Pick the answer that correctly identifies D-Labs' self-interested preferences regarding which type of trial to run and where to run it.",
        "options": ["(a) placebo-rich > active-rich > placebo-poor > active-poor", "(b) placebo-poor > active-poor > placebo-rich > active-rich", "(c) active-poor > placebo-poor > active-rich > placebo-rich", "(d) active-rich > active-poor > placebo-rich > placebo-poor"],
        "ans": "(a) placebo-rich > active-rich > placebo-poor > active-poor"
    },
    {
        "q": "Pick the answer that correctly ranks the moral goodness of those possibilities.",
        "options": ["(a) placebo-rich > active-rich > placebo-poor > active-poor", "(b) active-rich > active-poor > placebo-rich > placebo-poor", "(c) placebo-poor > active-poor > placebo-rich > active-rich"],
        "ans": "(b) active-rich > active-poor > placebo-rich > placebo-poor"
    },
    {
        "q": "The VIP Honda Civic Case: Handout #3.3 presents three principles about rights generation. The case presented in this question provides a compelling counterexample to all three of those principles.",
        "options": ["(a) True", "(b) False"],
        "ans": "(a) True"
    }
]

# --- SESSION STATE ---
def init_state():
    defaults = {
        'stage': 0, 'sub_stage': 0, 'learned_vocab': [], 
        'redo_queue': [], # Stores drills the user failed or asked for the answer to
        'drill_state': "unanswered", # unanswered, correct, wrong, show_ans
        'exam_score': 0, 'exam_q': 0, 'flashcards': list(vocab_defs.keys()),
        'fc_index': 0, 'fc_show_back': False, 'confirm_restart': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# Helpers
def next_stage(): 
    st.session_state.stage += 1
    st.session_state.sub_stage = 0
    st.session_state.drill_state = "unanswered"

def pass_mcq(vocab_words):
    st.session_state.sub_stage += 1
    st.session_state.drill_state = "unanswered"
    for w in vocab_words:
        if w not in st.session_state.learned_vocab:
            st.session_state.learned_vocab.append(w)

def check_spelling(user_input, valid_phrases):
    clean_in = re.sub(r'[^\w\s]', '', user_input).lower().strip()
    return any(re.sub(r'[^\w\s]', '', p).lower().strip() == clean_in for p in valid_phrases)

def add_to_redo(prompt, valid_phrases, exact_answer):
    drill_obj = {"prompt": prompt, "valid": valid_phrases, "exact": exact_answer}
    # Only add if not already in queue
    if not any(d["prompt"] == prompt for d in st.session_state.redo_queue):
        st.session_state.redo_queue.append(drill_obj)

# --- REUSABLE DRILL UI ---
def run_drill(prompt, valid_phrases, exact_answer, success_action=None):
    st.markdown(f"<div class='drill-box'><b>✏️ Drill:</b> {prompt}</div>", unsafe_allow_html=True)
    
    ans = st.text_input("Type your answer:", key=f"drill_{st.session_state.stage}_{st.session_state.sub_stage}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit Answer"):
            if check_spelling(ans, valid_phrases):
                st.session_state.drill_state = "correct"
            else:
                st.session_state.drill_state = "wrong"
                add_to_redo(prompt, valid_phrases, exact_answer)
    with col2:
        if st.button("I give up, Show Answer"):
            st.session_state.drill_state = "show_ans"
            add_to_redo(prompt, valid_phrases, exact_answer)
            
    if st.session_state.drill_state == "correct":
        st.success("✅ Correct! Beautiful spelling.")
        if st.button("Next 🐾"):
            if success_action: success_action()
            else: next_stage()
            st.rerun()
            
    elif st.session_state.drill_state == "wrong":
        st.error("❌ Not quite! The spelling or phrasing is off. Try again, or click 'Show Answer'. (Don't worry, if you struggle, we will just review it later!)")
        
    elif st.session_state.drill_state == "show_ans":
        st.info(f"🐻 **Professor Bear says:** The exact answer is **{exact_answer}**. \n\nI have added this to your review queue so we can practice it again before the exam!")
        if st.button("Acknowledge & Continue 🐾"):
            if success_action: success_action()
            else: next_stage()
            st.rerun()

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
    st.write("Welcome! We are going to roleplay through your exam material. You will have to make decisions in the shoes of the people involved.")
    st.write("If you misspell a word or get stuck on a drill, just hit 'Show Answer'. I will automatically save it and ask you again before you are allowed to take the Final Exam. Let's begin!")
    if st.button("Start Journey"): next_stage(); st.rerun()

# --- STAGE 1: Skepticism ---
elif st.session_state.stage == 1:
    st.title("Chapter 1: The Victim")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Your Situation:</b> You have an exam tomorrow. You step out of your dorm for a second. Your roommate maliciously flips the lock on your bathroom door. You go inside, and *click*. You are locked in for hours so they can ruin your grade and beat the curve!</div>", unsafe_allow_html=True)
        st.write("You are furious. You think, 'It is absolutely morally wrong for them to do this!'")
        st.write("But as a philosopher, you have to weigh the *reasons* against the *final verdict*. Which concept represents the final, absolute verdict that the action was impermissible?")
        
        if st.button("Moral Considerations"): st.error("❌ Nope! Those are just the 'weights on the scale' (e.g., 'It made me sad' vs 'It helped their grade'). Try again!")
        if st.button("All-Things-Considered Moral Norms"): pass_mcq(["Moral Considerations", "All-Things-Considered Moral Norms"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill(
            "What is the hyphenated phrase that represents the final, conclusive verdict of whether an action is morally impermissible?",
            ["all things considered moral norms", "all things considered", "allthingsconsidered"],
            "All-Things-Considered Moral Norms"
        )

# --- STAGE 2: Pogge & Clinical Trials ---
elif st.session_state.stage == 2:
    st.title("Chapter 2: The CEO of D-Lab")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Your Situation:</b> You are the CEO of D-Lab. You have a new drug, Surfaxin, for premature babies. You need to test it to get FDA approval. You have 4 options: <br>1. Active-Rich (test vs existing good drugs in US)<br>2. Active-Poor (test vs existing good drugs in Bolivia)<br>3. Placebo-Rich (test vs fake sugar water in US)<br>4. Placebo-Poor (test vs fake sugar water in Bolivia)</div>", unsafe_allow_html=True)
        st.write("As a greedy, self-interested company, what is your #1 preferred trial type? (Hint: smaller sample size, faster results)")
        
        if st.button("Active-Rich"): st.error("❌ Nope, that requires a massive sample size to prove your drug is *better* than an already great drug. Too expensive!")
        if st.button("Placebo-Rich"): 
            st.success("✅ Exactly! Placebo trials are cheap/fast, and 'rich' countries can actually afford to buy the drug once it's approved.")
            st.button("Continue the story...", on_click=lambda: setattr(st.session_state, 'sub_stage', 1))
            
    elif st.session_state.sub_stage == 1:
        st.markdown("<div class='story-box'><b>The Fallout:</b> You couldn't do Placebo-Rich because the US FDA banned placebo trials when a known cure exists. So you settled for Placebo-Poor in Bolivia.<br><br>The Bolivian parents are thanking you for 'treating' their babies, not realizing half of them are getting fake sugar water just so you can collect data!</div>", unsafe_allow_html=True)
        st.write("What is the term for when a participant confuses your goal (getting data) with a doctor's goal (saving patients)?")
        
        if st.button("Exception to Moral Freedom"): st.error("❌ Nope, that's Pogge's rule about exploitation. Try the other one!")
        if st.button("Therapeutic Misconception"): pass_mcq(["Therapeutic Misconception"]); st.rerun()

    elif st.session_state.sub_stage == 2:
        run_drill(
            "Type the two-word phrase for when a patient confuses a researcher for a doctor.",
            ["therapeutic misconception", "theraputic misconception"],
            "Therapeutic Misconception",
            success_action=lambda: setattr(st.session_state, 'sub_stage', 3)
        )
        
    elif st.session_state.sub_stage == 3:
        st.write("Professor Thomas Pogge shows up at your corporate office. He tells you the story of the Eccentric Filmmaker to prove a point: **You cannot exploit desperate people for your own ends, even if you are providing a net benefit.**")
        run_drill(
            "What is the name of Pogge's principle? (Exception to Moral _______)",
            ["exception to moral freedom", "moral freedom", "freedom"],
            "Exception to Moral Freedom"
        )

# --- STAGE 3: Thomson ---
elif st.session_state.stage == 3:
    st.title("Chapter 3: The Kidnapped Filter")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Your Situation:</b> You wake up in a hospital bed. The Society of Music Lovers kidnapped you and hooked your kidneys up to a famous violinist. If you unplug him now, he dies. He needs your body for 9 months.</div>", unsafe_allow_html=True)
        st.write("The violinist says, 'I have a Right to Life! Therefore, you are morally obligated to let me use your kidneys!' According to Thomson, is he right?")
        
        if st.button("Yes, Right to Life guarantees whatever you need to survive."): st.error("❌ Thomson argues this is a false definition of the Right to Life.")
        if st.button("No, Right to Life does NOT include the right to use another's body."): pass_mcq(["Right to Life (Thomson)", "Extreme View (EV)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.write("Because the violinist doesn't have a right to your body, Thomson proves that abortion isn't *always* impermissible.")
        run_drill(
            "What is the 2-word phrase for the view that abortion is ALWAYS impermissible, even to save the mother's life?",
            ["extreme view", "ev", "the extreme view"],
            "Extreme View (EV)"
        )

# --- STAGE 4: Marquis ---
elif st.session_state.stage == 4:
    st.title("Chapter 4: A Conversation with Marquis")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Your Situation:</b> You sit down with Don Marquis. He says, 'Forget religion. Forget the personhood debate. I'm going to prove abortion is wrong just by looking at you and me.' He asks: <i>Why is it wrong to kill you right now?</i></div>", unsafe_allow_html=True)
        
        if st.button("Because it causes pain."): st.error("❌ Too broad. What if you were under anesthesia?")
        if st.button("Because it deprives you of a valuable future."): pass_mcq(["A Future Like Ours (FLO)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill(
            "What is the exact phrase (or 3 letter acronym) Marquis uses to describe what a victim loses when they are killed?",
            ["a future like ours", "future like ours", "flo"],
            "A Future Like Ours (FLO)"
        )

# --- STAGE 5: Smart Review Gauntlet ---
elif st.session_state.stage == 5:
    st.title("🧠 The Redo Gauntlet")
    
    if len(st.session_state.redo_queue) == 0:
        st.success("🎉 You have cleared the Gauntlet! You proved you know all the vocabulary.")
        if st.button("Take Final Exam 📝"): 
            next_stage()
            st.rerun()
    else:
        st.warning(f"You have {len(st.session_state.redo_queue)} question(s) you need to master before taking the exam.")
        
        # Pull the first drill in the queue
        current_drill = st.session_state.redo_queue[0]
        st.markdown(f"<div class='drill-box'><b>✏️ Re-Test:</b> {current_drill['prompt']}</div>", unsafe_allow_html=True)
        
        redo_ans = st.text_input("Type the exact answer:", key="redo_input")
        
        if st.button("Submit Redo"):
            if check_spelling(redo_ans, current_drill['valid']):
                st.success("✅ Perfect! Removing this from your queue.")
                st.session_state.redo_queue.pop(0) # Remove it from the list
                st.button("Next Question", on_click=lambda: st.rerun())
            else:
                st.error("❌ Still not quite right. Read the sidebar definitions if you are stuck!")
                st.info(f"Reminder: The exact answer is **{current_drill['exact']}**")

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
        st.session_state.stage = 7
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
                    st.session_state.fc_index += 1
                    st.session_state.fc_show_back = False
                    st.rerun()
            with col2:
                if st.button("✅ I knew this"):
                    st.session_state.flashcards.pop(st.session_state.fc_index)
                    st.session_state.fc_show_back = False
                    st.rerun()
