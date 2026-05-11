import streamlit as st
import re
import random

# --- PAGE CONFIGURATION & THEME ---
st.set_page_config(page_title="Phil 4 Master Study App", page_icon="🐻", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f1ea; color: #3e2723; }
    h1, h2, h3 { color: #5d4037; font-family: 'Courier New', Courier, monospace; }
    .story-box { background-color: #e7cda2; padding: 20px; border-radius: 15px; border: 2px solid #8d6e63; margin-bottom: 20px; font-size: 18px; line-height: 1.6; }
    .vocab-box { background-color: #c8e6c9; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; margin-bottom: 15px; }
    .error-box { background-color: #ffcdd2; padding: 15px; border-radius: 10px; border-left: 5px solid #c62828; margin-bottom: 15px; }
    .drill-box { background-color: #bbdefb; padding: 15px; border-radius: 10px; border-left: 5px solid #1976d2; margin-bottom: 15px; }
    .flashcard { background-color: #ffffff; padding: 40px; border-radius: 15px; border: 3px dashed #8d6e63; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #795548; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #5d4037; color: #ffb300; }
    </style>
""", unsafe_allow_html=True)

# --- COURSE DATA & VOCAB ---
vocab_defs = {
    "Exception to Moral Freedom": "Pogge: You cannot exploit desperate people for your own ends, even if providing a net benefit.",
    "Extreme View (EV)": "Thomson 3.0: Abortion is ALWAYS impermissible.",
    "Slightly Less Extreme View (SLEV)": "Thomson 3.1: Abortion is impermissible EXCEPT to save the mother's life AND the mother must perform it herself.",
    "Moderate Pro-life View (Mod-pro)": "Thomson 3.2: Abortion is impermissible EXCEPT to save the mother's life (a doctor may perform it).",
    "Direct Killing Argument (DKA)": "Thomson 3.0/3.1: Premise 6.4 claims if options are directly killing an innocent or letting someone die, you must prefer letting them die.",
    "Right to Life (Thomson)": "Thomson 3.2: Does NOT include the right to be given the bare minimum one needs for continued life (like someone else's body).",
    "Moral Ownership": "Thomson 3.1: The mother morally owns her own body, which is why a third party/doctor is permitted to help her.",
    "Typical vs Emergency Cases": "Thomson 3.3: Emergency = mother will die. Typical = mother wants abortion for less weighty reasons.",
    "Rights Generators 1-4": "Thomson 3.3: Suggested ways a fetus might gain a right to the body. Disproved by the Identical Cars case.",
    "A Future Like Ours (FLO)": "Marquis: Killing is wrong because it deprives the victim of a valuable future."
}

# --- MASSIVE EXAM QUESTION BANK (Strictly from Notes) ---
all_exam_questions = [
    {
        "q": "According to Pogge, which of the following principles entails that it would have been wrong for D-Lab to run the clinical trial in Bolivia?",
        "options": ["(a) Moral Freedom", "(b) Moral Conditional", "(c) Moral Constraint", "(d) Exception to Moral Freedom", "(e) Moral Exploitation"],
        "ans": "(d) Exception to Moral Freedom",
        "exp": "Pogge specifically uses the Eccentric Filmmaker to demonstrate the 'Exception to Moral Freedom'—you cannot exploit desperate people even for a net benefit."
    },
    {
        "q": "Pick the answer that correctly identifies D-Labs' self-interested preferences regarding which type of trial to run.",
        "options": ["(a) placebo-rich > active-rich > placebo-poor > active-poor", "(b) placebo-poor > active-poor > placebo-rich > active-rich", "(c) active-rich > active-poor > placebo-rich > placebo-poor"],
        "ans": "(a) placebo-rich > active-rich > placebo-poor > active-poor",
        "exp": "D-Lab wants Placebo-rich first because placebos are cheap/fast, and rich countries can afford the drug later."
    },
    {
        "q": "Pick the answer that correctly ranks the moral goodness of those possibilities.",
        "options": ["(a) placebo-rich > active-rich > placebo-poor > active-poor", "(b) active-rich > active-poor > placebo-rich > placebo-poor", "(c) active-poor > placebo-poor > active-rich > placebo-rich"],
        "ans": "(b) active-rich > active-poor > placebo-rich > placebo-poor",
        "exp": "Morally speaking, providing 'active' (real) treatment to 'rich' or 'poor' is always better than giving a placebo."
    },
    {
        "q": "The VIP Honda Civic Case: Handout 3.3 presents three principles about rights generation. This case provides a compelling counterexample to all three of those principles.",
        "options": ["(a) True", "(b) False"],
        "ans": "(a) True",
        "exp": "True. The innocent driver accidentally taking your running Honda Civic disproves Rights Generators 1, 2, and 3, showing innocent arrival doesn't grant property rights."
    },
    {
        "q": "According to Thomson (Handout 3.0), what does the Extreme View (EV) claim?",
        "options": ["(a) Abortion is always impermissible.", "(b) Abortion is impermissible unless the mother's life is at risk.", "(c) Abortion is only permissible if performed by the mother herself."],
        "ans": "(a) Abortion is always impermissible.",
        "exp": "EV allows NO exceptions whatsoever, not even to save the mother's life."
    },
    {
        "q": "According to Thomson (Handout 3.1), what does the Slightly Less Extreme View (SLEV) claim?",
        "options": ["(a) Abortion is always impermissible.", "(b) A mother may abort to save her life, but a doctor/third party may not perform it.", "(c) A doctor may perform an emergency abortion."],
        "ans": "(b) A mother may abort to save her life, but a doctor/third party may not perform it.",
        "exp": "SLEV allows the mother to save herself, but explicitly forbids third parties (doctors) from intervening."
    },
    {
        "q": "In Handout 3.1, Thomson uses the 'Chet & Abilene (Bus) Case' as a counterexample. What argument is it attacking?",
        "options": ["(a) The Basic Right to Life Argument", "(b) Marquis's FLO", "(c) The Direct Killing Argument (DKA)"],
        "ans": "(c) The Direct Killing Argument (DKA)",
        "exp": "The Bus Case (where a passenger falls on you and you will die unless you push them off) is used to attack Premise 6.4 of the DKA, which says you must let yourself die rather than directly kill an innocent."
    },
    {
        "q": "According to Thomson (Handout 3.2), what does the Moderate Pro-Life View (Mod-pro) claim?",
        "options": ["(a) Abortion is always impermissible.", "(b) Abortion is impermissible except to save the mother's life.", "(c) Abortion is permissible for any reason."],
        "ans": "(b) Abortion is impermissible except to save the mother's life.",
        "exp": "Mod-pro allows a doctor to perform the abortion to save the mother's life, but forbids it in typical, non-emergency cases."
    },
    {
        "q": "In the Second Version of the Right to Life Argument (Handout 3.2), Premise 4 states that a fetus's right to life trumps any other considerations EXCEPT...",
        "options": ["(a) The mother's right to bodily autonomy", "(b) The mother's right to life", "(c) The fetus's future like ours"],
        "ans": "(b) The mother's right to life",
        "exp": "Premise 4 of the 2nd RtL Argument states that the fetus's right to life trumps everything *with the possible exception of the mother's right to life*."
    },
    {
        "q": "According to Thomson (Handout 3.2), the 'Right to Life' does NOT include:",
        "options": ["(a) The right not to be killed maliciously.", "(b) The right to be given the bare minimum one needs for continued life.", "(c) The right to a valuable future."],
        "ans": "(b) The right to be given the bare minimum one needs for continued life.",
        "exp": "This is Thomson's core point: Even if the Violinist has a right to life, it doesn't mean he has the right to the 'bare minimum' (use of your kidneys) needed to survive."
    },
    {
        "q": "According to Thomson (Handout 3.3), in 'Typical Cases' (unlike Emergency Cases), the mother's life is not in danger. Thomson argues abortion is still permissible because:",
        "options": ["(a) The fetus is not a person.", "(b) The mother would have to make a 'large sacrifice' to allow use of her body, and the fetus has no right against her to demand it.", "(c) The direct killing argument is murder."],
        "ans": "(b) The mother would have to make a 'large sacrifice' to allow use of her body, and the fetus has no right against her to demand it.",
        "exp": "Thomson's Argument for Permissibility (Handout 3.3) states if A has to make a 'large sacrifice' to save B, and B has no right to demand it, A is not morally required to do so."
    },
    {
        "q": "What is the primary philosophical point of Thomson's Basic Violinist Case?",
        "options": ["(a) To prove fetuses are not persons.", "(b) To prove that the Right to Life does not guarantee the right to use another person's body.", "(c) To prove that abortion is always permissible."],
        "ans": "(b) To prove that the Right to Life does not guarantee the right to use another person's body.",
        "exp": "The Violinist is Thomson's most famous analogy proving that the right to life does not entail a right to use someone's body without their continuous consent."
    },
    {
        "q": "What does Marquis identify as the primary reason killing an adult human is wrong?",
        "options": ["(a) It directly kills an innocent person.", "(b) It deprives the victim of a Future Like Ours (FLO).", "(c) It violates their bodily autonomy."],
        "ans": "(b) It deprives the victim of a Future Like Ours (FLO).",
        "exp": "Marquis explicitly argues that the wrongness of killing stems from depriving the victim of all the experiences and joys of a valuable future."
    },
    {
        "q": "Thomson argues that a third party (a doctor) CAN intervene to save a mother's life in an emergency abortion. What concept from Handout 3.1 justifies the doctor intervening?",
        "options": ["(a) The Exception to Moral Freedom", "(b) Moral Ownership", "(c) The Therapeutic Misconception"],
        "ans": "(b) Moral Ownership",
        "exp": "Thomson argues that the mother 'morally owns' her body, which gives her the right to authorize a third party (the doctor) to assist her."
    },
    {
        "q": "According to Marquis, his 'Future Like Ours' argument is superior to other anti-abortion arguments because it avoids the 'usual equivocations' on what terms?",
        "options": ["(a) 'Direct killing' and 'letting die'", "(b) 'Human life' and 'person'", "(c) 'Moral considerations' and 'moral norms'"],
        "ans": "(b) 'Human life' and 'person'",
        "exp": "Marquis notes on page 1 of his essay that FLO avoids getting bogged down in messy debates over the exact definition of a 'person' or 'human life'."
    },
    {
        "q": "Handout 3.1 discusses three ways a counterexample can be used against the Direct Killing Argument (DKA). Which of the following is the 'Esmerelda' case used for?",
        "options": ["(a) To attack the premise that fetuses are innocent.", "(b) To attack Premise 6.4 (that you must let yourself die rather than directly kill).", "(c) To prove that Ontological Moral Skepticism is true."],
        "ans": "(b) To attack Premise 6.4 (that you must let yourself die rather than directly kill).",
        "exp": "Esmerelda (and the Bus Case) are counterexamples proving that you are NOT morally required to sit back and let yourself die if an innocent threat is going to crush you."
    },
    {
        "q": "In the Roommate Case (Handout 1.0), what is the distinction Professor McHose emphasizes?",
        "options": ["(a) Active-rich vs. Placebo-poor", "(b) EV vs. SLEV", "(c) Moral Considerations vs. All-Things-Considered Moral Norms"],
        "ans": "(c) Moral Considerations vs. All-Things-Considered Moral Norms",
        "exp": "The roommate case separates the individual reasons (considerations) from the final verdict of impermissibility (norms)."
    },
    {
        "q": "Which of the following is a key element of the Direct Killing Argument (DKA)?",
        "options": ["(a) Letting someone die is worse than directly killing them.", "(b) Directly killing an innocent person is worse than letting someone die.", "(c) A fetus has no right to life."],
        "ans": "(b) Directly killing an innocent person is worse than letting someone die.",
        "exp": "The DKA relies on the idea that actively, directly killing the fetus is a worse moral action than passively letting the mother die."
    },
    {
        "q": "If a woman wants an abortion simply because she does not want to be a parent right now, which category of cases does Thomson place this in (Handout 3.3)?",
        "options": ["(a) Emergency Cases", "(b) Typical Cases", "(c) Rights Generator Cases"],
        "ans": "(b) Typical Cases",
        "exp": "Emergency cases are life-or-death. Thomson defines 'Typical Cases' as vastly more common cases where the reason is less weighty than preserving her own life."
    },
    {
        "q": "According to Pogge's Exception to Moral Freedom, if a corporation provides a 'net benefit' to a desperate population, are they automatically morally justified?",
        "options": ["(a) Yes, a net benefit is all that is required.", "(b) No, providing a net benefit does not give you the right to exploit their desperation.", "(c) Yes, because of the Therapeutic Misconception."],
        "ans": "(b) No, providing a net benefit does not give you the right to exploit their desperation.",
        "exp": "The Eccentric Filmmaker provides a net benefit (cash), but Pogge says his actions are still grotesque because he is exploiting their desperation."
    }
]

# --- SESSION STATE ---
def init_state():
    defaults = {
        'stage': 0, 'sub_stage': 0, 'learned_vocab': [], 
        'redo_queue': [], 'drill_state': "unanswered",
        'exam_score': 0, 'exam_q_index': 0, 
        'active_exam_pool': [], 'q_answered_correctly': False,
        'flashcards': list(vocab_defs.keys()),
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
    if not any(d["prompt"] == prompt for d in st.session_state.redo_queue):
        st.session_state.redo_queue.append(drill_obj)

def run_drill(prompt, valid_phrases, exact_answer, success_action=None):
    st.markdown(f"<div class='drill-box'><b>✏️ Drill to remember:</b><br>{prompt}</div>", unsafe_allow_html=True)
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
        if st.button("Next Chapter 🐾"):
            if success_action: success_action()
            else: next_stage()
            st.rerun()
    elif st.session_state.drill_state == "wrong":
        st.error("❌ Not quite! The spelling or phrasing is off. Try again, or click 'Show Answer'.")
    elif st.session_state.drill_state == "show_ans":
        st.info(f"🐻 **Professor Bear says:** The exact answer is **{exact_answer}**. I added this to your review queue!")
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
st.sidebar.markdown("### 📚 Known Vocab Dictionary")
for word in st.session_state.learned_vocab:
    with st.sidebar.expander(f"✅ {word}"):
        st.write(vocab_defs[word])

# --- STAGE 0: Intro ---
if st.session_state.stage == 0:
    st.title("🐻 Phil 4 Master Study App")
    st.write("Welcome! We are going through your EXACT study guide bullet points (Pogge, Thomson Handouts 3.0-3.3, and Marquis).")
    if st.button("Start Journey"): next_stage(); st.rerun()

# --- STAGE 1: Pogge (Handout 2.2) ---
elif st.session_state.stage == 1:
    st.title("Chapter 1: Pogge (Handout 2.2)")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Study Guide Topic:</b> Pogge Handout 2.2 p10-17.<br><br><b>Scenario:</b> D-Lab is testing Surfaxin in Bolivia using a placebo-poor trial. Pogge argues this is wrong using the 'Eccentric Filmmaker' case. The filmmaker gives starving people a 50/50 chance at $30,000 or a paint-bomb. Even though he provides a 'net benefit' (money) to the town, his conduct is grotesque.</div>", unsafe_allow_html=True)
        st.write("What specific principle does the Eccentric Filmmaker prove regarding exploiting desperate people?")
        
        if st.button("Moral Conditional"): st.error("❌ Incorrect.")
        if st.button("Exception to Moral Freedom"): pass_mcq(["Exception to Moral Freedom"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill("What is the exact name of Pogge's principle? (Hint: Exception to Moral _______)", ["exception to moral freedom", "moral freedom"], "Exception to Moral Freedom")

# --- STAGE 2: Thomson (Handout 3.0) ---
elif st.session_state.stage == 2:
    st.title("Chapter 2: Thomson (Handout 3.0)")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Study Guide Topics:</b> Basic RtL, Basic Violinist, EV, DKA.<br><br><b>Scenario:</b> You wake up hooked to a famous violinist. The Society of Music Lovers says his 'Right to Life' means you MUST let him use your kidneys for 9 months. Thomson says NO. Therefore, the <b>Extreme View (EV)</b> (which says abortion is ALWAYS impermissible, even to save the mother) is false.</div>", unsafe_allow_html=True)
        st.write("Does Thomson believe the Right to Life includes the right to use another person's body to survive?")
        if st.button("Yes"): st.error("❌ No, Thomson argues this is a false assumption by pro-life advocates.")
        if st.button("No"): pass_mcq(["Extreme View (EV)", "Right to Life (Thomson)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill("What is the 2-word phrase for the view that abortion is ALWAYS impermissible?", ["extreme view", "ev"], "Extreme View (EV)")

# --- STAGE 3: Thomson (Handout 3.1) ---
elif st.session_state.stage == 3:
    st.title("Chapter 3: Thomson (Handout 3.1)")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Study Guide Topics:</b> DKA Counterexamples, Bus Case, SLEV, Moral Ownership.<br><br><b>Scenario:</b> The Direct Killing Argument (DKA) says you must let yourself die rather than directly kill an innocent. Thomson attacks this with the <b>Bus Case (Chet & Abilene)</b>: If a passenger falls on you and will crush you to death, are you morally required to let them crush you? No, you can push them off! <br><br>Also, under the <b>Slightly Less Extreme View (SLEV)</b>, a mother can abort to save her life, but a doctor cannot help her. Thomson attacks this using <b>Moral Ownership</b>: The mother owns her body, so she can authorize a doctor to help her.</div>", unsafe_allow_html=True)
        st.write("Under SLEV, is a doctor allowed to perform an emergency abortion?")
        if st.button("Yes"): st.error("❌ No! SLEV says only the mother can perform it.")
        if st.button("No"): pass_mcq(["Slightly Less Extreme View (SLEV)", "Direct Killing Argument (DKA)", "Moral Ownership"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill("What concept explains why a mother can authorize a third-party doctor to help her? (Hint: Moral _________)", ["moral ownership", "ownership"], "Moral Ownership")

# --- STAGE 4: Thomson (Handouts 3.2 & 3.3) ---
elif st.session_state.stage == 4:
    st.title("Chapter 4: Thomson (Handouts 3.2 & 3.3)")
    
    if st.session_state.sub_stage == 0:
        st.markdown("<div class='story-box'><b>Study Guide Topics:</b> Mod-pro, 2nd Version RtL, Typical vs Emergency, Rights Generators, Identical Cars.<br><br><b>Scenario:</b> In <b>Typical Cases</b> (where the mother's life is NOT in danger), Thomson argues that if the mother must make a 'large sacrifice', she is not morally required to do so.<br><br>Some argue a fetus gains a right to the body via intercourse (Rights Generators 1-4). Thomson disproves this with the <b>VIP Honda Civic (Identical Cars)</b> case: Just because an innocent guy mistakenly gets into your running car doesn't mean he gets a moral right to keep it!</div>", unsafe_allow_html=True)
        st.write("What view states that abortion is impermissible EXCEPT to save the mother's life (and a doctor CAN perform it)?")
        if st.button("Moderate Pro-Life View (Mod-pro)"): pass_mcq(["Moderate Pro-life View (Mod-pro)", "Typical vs Emergency Cases", "Rights Generators 1-4"]); st.rerun()
        if st.button("Extreme View"): st.error("❌ EV allows NO exceptions.")

    elif st.session_state.sub_stage == 1:
        run_drill("The Honda Civic case is used to disprove Rights Generators 1-4. What do we call a scenario that disproves a rule?", ["counterexample", "counter example"], "Counterexample")

# --- STAGE 5: Smart Review Gauntlet ---
elif st.session_state.stage == 5:
    st.title("🧠 The Redo Gauntlet")
    if len(st.session_state.redo_queue) == 0:
        st.success("🎉 You cleared the Gauntlet! Time for the Final Exam.")
        if st.button("Take Final Exam 📝"): next_stage(); st.rerun()
    else:
        st.warning(f"You have {len(st.session_state.redo_queue)} question(s) to master before the exam.")
        current_drill = st.session_state.redo_queue[0]
        st.markdown(f"<div class='drill-box'><b>✏️ Re-Test:</b><br>{current_drill['prompt']}</div>", unsafe_allow_html=True)
        redo_ans = st.text_input("Type the exact answer:", key="redo_input")
        if st.button("Submit Redo"):
            if check_spelling(redo_ans, current_drill['valid']):
                st.success("✅ Perfect!")
                st.session_state.redo_queue.pop(0)
                st.button("Next Question", on_click=lambda: st.rerun())
            else:
                st.error(f"❌ Still not quite right. Reminder: The answer is **{current_drill['exact']}**")

# --- STAGE 6: FINAL EXAM (Strict & Randomized) ---
elif st.session_state.stage == 6:
    st.title("📝 The Final Exam (20 Questions)")
    st.write("You must get each question correct to proceed. Explanations provided on failure.")
    
    # Initialize the random pool of 20 questions exactly once
    if not st.session_state.active_exam_pool:
        st.session_state.active_exam_pool = random.sample(all_exam_questions, 20)
        st.session_state.exam_q_index = 0
        st.session_state.q_answered_correctly = False

    # Check if finished
    if st.session_state.exam_q_index >= 20:
        st.success("🎉 YOU PASSED THE FINAL EXAM!")
        if st.button("Go to Flashcards"): next_stage(); st.rerun()
    else:
        q_data = st.session_state.active_exam_pool[st.session_state.exam_q_index]
        st.markdown(f"**Question {st.session_state.exam_q_index + 1} of 20**")
        st.write(q_data["q"])
        
        if not st.session_state.q_answered_correctly:
            for opt in q_data["options"]:
                if st.button(opt):
                    if opt == q_data["ans"]:
                        st.success("✅ Correct!")
                        st.session_state.q_answered_correctly = True
                        st.rerun()
                    else:
                        st.error(f"❌ Incorrect. \n\n**Why?** {q_data['exp']}")
        else:
            st.success(f"**Explanation:** {q_data['exp']}")
            if st.button("Next Question ➡️"):
                st.session_state.exam_q_index += 1
                st.session_state.q_answered_correctly = False
                st.rerun()

# --- STAGE 7: FLASHCARDS ---
elif st.session_state.stage == 7:
    st.title("🃏 Mastery Flashcards")
    if len(st.session_state.flashcards) == 0:
        st.balloons()
        st.success("You mastered every card! You are ready for Exam 2.")
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
