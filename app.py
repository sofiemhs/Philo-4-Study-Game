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

# --- COURSE DATA (Strictly from Notes) ---
vocab_defs = {
    "Ontological Moral Skepticism (OMS)": "The belief that there are no moral facts at all (e.g., nothing is truly 'wrong'). Professor McHose argues that cases like the Evil Roommate make this view seem absurd.",
    "Moral Considerations": "The individual factors that weigh for or against an action (a.k.a moral reasons). These are just the 'weights on the scale'.",
    "All-Things-Considered Moral Norms": "The final, conclusive verdict of whether an action is wrong or morally impermissible after weighing all the moral considerations.",
    "Therapeutic Misconception": "When a participant in a clinical trial confuses a researcher's main goal (to get information) with a doctor's main goal (to preserve patient health).",
    "Exception to Moral Freedom": "Pogge's principle: You cannot exploit desperate people for your own ends, even if you are providing them with a net benefit (demonstrated by the Eccentric Filmmaker case).",
    "Extreme View (EV)": "The pro-life view that abortion is ALWAYS impermissible, even to save the mother's life.",
    "Slightly Less Extreme View (SLEV)": "Abortion is impermissible EXCEPT to save the mother's life, AND the mother must perform it herself (a doctor/third party may not).",
    "Right to Life (Thomson's definition)": "The right to not be killed unjustly. It does NOT include the right to be given the bare minimum one needs for continued life (such as the use of another person's body).",
    "Counterexample": "A specific scenario used in philosophy to disprove a general rule or principle (e.g., the VIP Honda Civic case disproves Rights Generators 1-3).",
    "A Future Like Ours (FLO)": "Don Marquis's argument that killing an adult is wrong because it deprives the victim of a valuable future. He argues that fetuses also possess this property, making abortion wrong."
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
        'redo_queue': [], 'drill_state': "unanswered",
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
    if not any(d["prompt"] == prompt for d in st.session_state.redo_queue):
        st.session_state.redo_queue.append(drill_obj)

# --- REUSABLE DRILL UI ---
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
st.sidebar.markdown("### 📚 Known Vocab Dictionary")
for word in st.session_state.learned_vocab:
    with st.sidebar.expander(f"✅ {word}"):
        st.write(vocab_defs[word])

# --- STAGE 0: Intro ---
if st.session_state.stage == 0:
    st.title("🐻 Phil 4 Master Study App")
    st.write("Welcome! We are going to roleplay through your exam material. You will have to make decisions in the shoes of the people involved.")
    st.write("If you misspell a word or get stuck on a drill, just hit 'Show Answer'. I will automatically save it and ask you again before you are allowed to take the Final Exam. Let's begin!")
    if st.button("Start Journey"): next_stage(); st.rerun()

# --- STAGE 1: Skepticism (Handouts 1.0 & 1.1) ---
elif st.session_state.stage == 1:
    st.title("Chapter 1: The Evil Roommate & Moral Facts")
    
    if st.session_state.sub_stage == 0:
        st.markdown("""
        <div class='story-box'>
        <b>The Scenario:</b><br>
        Imagine you have a huge philosophy exam tomorrow. You step out of your dorm for a second. Your roommate maliciously flips the lock on your bathroom door. You go inside, and *click*. You are locked in for hours so they can ruin your grade, beat the curve, and get an A. 
        <br><br>
        <b>The Philosophy:</b><br>
        Almost every human being on earth agrees that what your roommate did was "wrong." However, there is a philosophical view called <b>Ontological Moral Skepticism (OMS)</b> which claims that <i>there are absolutely no moral facts in the universe</i>. If OMS is true, then your belief that your roommate was wrong is actually a false belief! Professor McHose uses this highly relatable case to show that OMS is a very jarring and counterintuitive way to view the world.
        </div>
        """, unsafe_allow_html=True)
        st.write("When deciding if the roommate was wrong, Professor McHose says we must separate two things. One is the 'little weights on the scale' (e.g., 'It hurt your grade' vs. 'It helped their grade'). What do we call these little weights/reasons?")
        
        if st.button("All-Things-Considered Moral Norms"): st.error("❌ Nope! That is the *final verdict*, not the individual weights/reasons. Try again!")
        if st.button("Moral Considerations"): pass_mcq(["Ontological Moral Skepticism (OMS)", "Moral Considerations"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.write("Excellent. So 'Moral Considerations' are the reasons for or against an action. But after we weigh all those reasons, we come to a final verdict (e.g., 'Locking you in the bathroom was 100% impermissible').")
        run_drill(
            "What is the hyphenated phrase that represents the final, conclusive verdict of whether an action is morally impermissible?",
            ["all things considered moral norms", "all things considered", "allthingsconsidered"],
            "All-Things-Considered Moral Norms",
            success_action=lambda: [pass_mcq(["All-Things-Considered Moral Norms"]), next_stage()]
        )

# --- STAGE 2: Clinical Trials (Handout 2.0) ---
elif st.session_state.stage == 2:
    st.title("Chapter 2: The CEO of D-Lab")
    
    if st.session_state.sub_stage == 0:
        st.markdown("""
        <div class='story-box'>
        <b>The Scenario:</b><br>
        You are the CEO of a pharmaceutical company called "D-Lab." You have a new drug called Surfaxin that helps premature babies breathe. You need to run a "Randomized Control Trial" to see if it works. 
        <br><br>
        You have four options for your trial:<br>
        1. <b>Active-Rich:</b> Run the trial in a rich country (US) and compare Surfaxin against the best *already existing* drug.<br>
        2. <b>Active-Poor:</b> Run it in a poor country (Bolivia) against the best existing drug.<br>
        3. <b>Placebo-Rich:</b> Run it in a rich country and compare Surfaxin against a <i>placebo</i> (fake sugar water).<br>
        4. <b>Placebo-Poor:</b> Run it in a poor country against a placebo.<br><br>
        <b>The Philosophy:</b><br>
        Placebo trials are much cheaper and require fewer participants because the difference between a real drug and sugar water is obvious quickly. Also, rich countries are preferred by companies because their citizens can actually afford to buy the drug once it is approved. 
        </div>
        """, unsafe_allow_html=True)
        st.write("Based on this, if you are a greedy CEO looking out *only* for your self-interest, how do you rank your trial preferences (from best to worst)?")
        
        if st.button("Active-Rich > Active-Poor > Placebo-Rich > Placebo-Poor"): st.error("❌ Nope, Active trials require massive sample sizes to prove your drug is *better* than an already great drug. Too expensive!")
        if st.button("Placebo-Rich > Active-Rich > Placebo-Poor > Active-Poor"): pass_mcq([]); st.rerun()
            
    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='story-box'>
        <b>The Fallout:</b><br>
        You couldn't do a "Placebo-Rich" trial because the US FDA bans using placebos on babies when a known cure already exists! So, you settle for a "Placebo-Poor" trial in Bolivia because they have looser laws.<br><br>
        When you arrive in Bolivia, the parents are weeping with joy. They are thanking you for "treating" their dying babies. What they don't realize is that you are a <i>researcher</i>, not a doctor. Half of these babies are getting fake sugar water just so you can collect data, and you have no intention of saving them all.
        </div>
        """, unsafe_allow_html=True)
        st.write("What is the psychological term for when a participant confuses a researcher's goal (getting data) with a doctor's goal (saving patients)?")
        
        if st.button("Exception to Moral Freedom"): st.error("❌ Nope, that's Pogge's rule about exploitation. Try the other one!")
        if st.button("Therapeutic Misconception"): pass_mcq(["Therapeutic Misconception"]); st.rerun()

    elif st.session_state.sub_stage == 2:
        run_drill(
            "Type the exact two-word phrase for when a patient incorrectly believes a clinical trial is designed purely to heal them.",
            ["therapeutic misconception", "theraputic misconception"],
            "Therapeutic Misconception"
        )

# --- STAGE 3: Pogge (Handouts 2.1 & 2.2) ---
elif st.session_state.stage == 3:
    st.title("Chapter 3: The Eccentric Filmmaker")
    
    if st.session_state.sub_stage == 0:
        st.markdown("""
        <div class='story-box'>
        <b>The Scenario:</b><br>
        Philosopher Thomas Pogge hears about your D-Lab trial in Bolivia and decides to teach you a lesson. He tells you a story about an "Eccentric Filmmaker."<br><br>
        A rich, twisted filmmaker goes to a desperately poor neighborhood. He has a truck full of unmarked boxes. Half the boxes contain $30,000. The other half contain a violent paint-bomb. He tells the poor residents: <i>"If you consent, I will flip a coin. Heads, you get a box with money. Tails, you get a paint-bomb to the face. I am filming this for my own amusement."</i><br><br>
        Because the residents are starving and desperate, many agree to play. Overall, the filmmaker is actually providing a "net benefit" to the neighborhood (bringing in lots of money).
        </div>
        """, unsafe_allow_html=True)
        st.write("Does Pogge believe that the Eccentric Filmmaker's actions are morally acceptable just because the poor people 'consented' and received a net benefit?")
        
        if st.button("Yes, because it's their choice and they got money."): st.error("❌ No! Pogge believes the filmmaker's behavior is grotesque and wrong.")
        if st.button("No, you cannot exploit desperation for your own amusement/profit."): pass_mcq([]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='story-box'>
        <b>The Philosophy:</b><br>
        Pogge uses the Filmmaker story as an analogy for D-Lab's Surfaxin trial in Bolivia. Even though D-Lab is giving <i>some</i> babies medicine (a net benefit), they are taking advantage of the Bolivians' desperate poverty to run a cheap placebo trial that they couldn't run in the US.
        </div>
        """, unsafe_allow_html=True)
        st.write("What is the name of Pogge's specific principle which states that you cannot exploit desperate people for your own ends?")
        
        if st.button("Moral Conditional"): st.error("❌ Incorrect. Think about the word 'Exception'.")
        if st.button("Exception to Moral Freedom"): pass_mcq(["Exception to Moral Freedom"]); st.rerun()

    elif st.session_state.sub_stage == 2:
        run_drill(
            "What is the exact name of Pogge's principle regarding exploitation? (Hint: Exception to Moral _______)",
            ["exception to moral freedom", "moral freedom", "freedom"],
            "Exception to Moral Freedom"
        )

# --- STAGE 4: Thomson (Handouts 3.0, 3.1, 3.2) ---
elif st.session_state.stage == 4:
    st.title("Chapter 4: The Kidnapped Filter (Thomson)")
    
    if st.session_state.sub_stage == 0:
        st.markdown("""
        <div class='story-box'>
        <b>The Scenario:</b><br>
        We now transition to the ethics of Abortion. Philosopher Judith Jarvis Thomson asks you to imagine the following:<br><br>
        You wake up in a hospital bed. You have been kidnapped by the "Society of Music Lovers." Next to you is a famously talented violinist who is dying of a kidney ailment. The Society has plugged his circulatory system into yours. If you unplug him right now, he dies. He needs to use your kidneys for 9 months to survive.<br><br>
        <b>The Philosophy:</b><br>
        Pro-life advocates argue that a fetus has a "Right to Life," which overrides the mother's right to her body. The violinist also clearly has a "Right to Life." But does his right to life mean you are <i>morally obligated</i> to lay in that bed for 9 months?
        </div>
        """, unsafe_allow_html=True)
        st.write("According to Thomson, does the Violinist's 'Right to Life' give him the right to use your kidneys?")
        
        if st.button("Yes, Right to Life guarantees whatever you need to survive."): st.error("❌ Thomson argues this is a false definition of the Right to Life.")
        if st.button("No, Right to Life does NOT include the right to use another's body."): pass_mcq(["Right to Life (Thomson's definition)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='story-box'>
        <b>The Philosophy:</b><br>
        Because the violinist doesn't have a right to your body, Thomson proves that having a "Right to Life" doesn't automatically make it impermissible to unplug him (or, by analogy, to have an abortion).<br><br>
        Thomson strictly defines the views of her opponents:<br>
        1. <b>The Extreme View (EV):</b> Abortion is ALWAYS impermissible, even to save the mother's life.<br>
        2. <b>The Slightly Less Extreme View (SLEV):</b> Abortion is impermissible EXCEPT to save the mother's life, BUT only the mother herself can perform it. A doctor (a third party) is not allowed to intervene.
        </div>
        """, unsafe_allow_html=True)
        st.write("Under the 'Slightly Less Extreme View (SLEV)', can a doctor perform a life-saving abortion on a mother?")
        
        if st.button("Yes, if it saves her life."): st.error("❌ No, SLEV strictly forbids third-party intervention.")
        if st.button("No, only the mother can perform it herself."): pass_mcq(["Extreme View (EV)", "Slightly Less Extreme View (SLEV)"]); st.rerun()

    elif st.session_state.sub_stage == 2:
        run_drill(
            "What is the 2-word phrase for the view that abortion is ALWAYS impermissible, with absolutely no exceptions?",
            ["extreme view", "ev", "the extreme view"],
            "Extreme View (EV)"
        )

# --- STAGE 5: Thomson (Handout 3.3) ---
elif st.session_state.stage == 5:
    st.title("Chapter 5: The VIP Honda Civic")
    
    if st.session_state.sub_stage == 0:
        st.markdown("""
        <div class='story-box'>
        <b>The Scenario:</b><br>
        Some people argue that if a mother engages in intercourse (even with contraception), she is partially responsible for the fetus existing, and thus she "generates a right" for the fetus to use her body. Thomson attacks this with the Honda Civic case:<br><br>
        You pay for VIP parking at a concert. A gang of sophisticated thieves breaks in and steals cars. They open your Honda Civic and leave it running, but get spooked by cops and run away. An innocent concert-goer walks out, sees your running Honda Civic, thinks it is his identical car, gets in, and drives away. <br><br>
        <b>The Philosophy:</b><br>
        The innocent driver is like the fetus. He didn't do anything malicious. He just arrived there by accident due to a chain of events. But does he now have a <i>moral right</i> to keep your car? No! 
        </div>
        """, unsafe_allow_html=True)
        st.write("Professor McHose uses this specific story to completely disprove the philosophical rule that 'innocent arrival guarantees a right to use property'. In logic, what do we call a scenario that disproves a rule?")
        
        if st.button("A Direct Killing Argument"): st.error("❌ Nope, that is a different concept regarding murder.")
        if st.button("A Counterexample"): pass_mcq(["Counterexample"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill(
            "Type the exact word for a scenario that disproves a philosophical rule (e.g., the Honda Civic case disproves Rights Generators 1, 2, and 3).",
            ["counterexample", "counter example"],
            "Counterexample"
        )

# --- STAGE 6: Marquis (Handout 4) ---
elif st.session_state.stage == 6:
    st.title("Chapter 6: A Conversation with Marquis")
    
    if st.session_state.sub_stage == 0:
        st.markdown("""
        <div class='story-box'>
        <b>The Scenario:</b><br>
        You sit down with philosopher Don Marquis. He says, "The abortion debate is stuck. People argue forever about whether a fetus is a 'person' or a 'cluster of cells', or they argue about religion. I am going to ignore all of that."<br><br>
        Instead, Marquis asks a simple question: <i>"Why is it wrong to kill you, an adult human being, right now?"</i><br><br>
        <b>The Philosophy:</b><br>
        Marquis answers his own question: Killing you is wrong because it deprives you of all the experiences, joys, and projects of your future. Since a fetus also possesses this exact same property (a valuable future waiting for it), killing a fetus is in the exact same moral category as killing an adult human being.
        </div>
        """, unsafe_allow_html=True)
        st.write("According to Marquis, what is the primary reason that killing an adult is wrong?")
        
        if st.button("Because it causes pain."): st.error("❌ Too broad. What if the adult was killed instantly in their sleep with no pain?")
        if st.button("Because it deprives the victim of a valuable future."): pass_mcq(["A Future Like Ours (FLO)"]); st.rerun()

    elif st.session_state.sub_stage == 1:
        run_drill(
            "What is the exact 4-word phrase (or 3-letter acronym) Marquis uses to describe what a victim loses when they are killed?",
            ["a future like ours", "future like ours", "flo"],
            "A Future Like Ours (FLO)"
        )

# --- STAGE 7: Smart Review Gauntlet ---
elif st.session_state.stage == 7:
    st.title("🧠 The Redo Gauntlet")
    
    if len(st.session_state.redo_queue) == 0:
        st.success("🎉 You have cleared the Gauntlet! You proved you know all the vocabulary.")
        if st.button("Take Final Exam 📝"): 
            next_stage()
            st.rerun()
    else:
        st.warning(f"You have {len(st.session_state.redo_queue)} question(s) you need to master before taking the exam.")
        
        current_drill = st.session_state.redo_queue[0]
        st.markdown(f"<div class='drill-box'><b>✏️ Re-Test:</b><br>{current_drill['prompt']}</div>", unsafe_allow_html=True)
        
        redo_ans = st.text_input("Type the exact answer:", key="redo_input")
        
        if st.button("Submit Redo"):
            if check_spelling(redo_ans, current_drill['valid']):
                st.success("✅ Perfect! Removing this from your queue.")
                st.session_state.redo_queue.pop(0)
                st.button("Next Question", on_click=lambda: st.rerun())
            else:
                st.error("❌ Still not quite right. Read the sidebar definitions if you are stuck!")
                st.info(f"Reminder: The exact answer is **{current_drill['exact']}**")

# --- STAGE 8: FINAL EXAM ---
elif st.session_state.stage == 8:
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
        st.session_state.stage = 9
        st.rerun()

# --- STAGE 9: EXAM RESULTS ---
elif st.session_state.stage == 9:
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
            st.session_state.stage = 8
            st.rerun()

# --- STAGE 10: FLASHCARDS ---
elif st.session_state.stage == 10:
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
