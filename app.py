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
    .drill-box { background-color: #bbdefb; padding: 15px; border-radius: 10px; border-left: 5px solid #1976d2; margin-bottom: 15px; }
    .exam-box { background-color: #e1bee7; padding: 20px; border-radius: 10px; border: 3px solid #8e24aa; margin-bottom: 15px; }
    .flashcard { background-color: #ffffff; padding: 40px; border-radius: 15px; border: 3px dashed #8d6e63; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #795548; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #5d4037; color: #ffb300; }
    </style>
""", unsafe_allow_html=True)

# --- VOCABULARY ---
vocab_defs = {
    "Exception to Moral Freedom": "Pogge: You cannot exploit desperate people for your own ends, even if providing a net benefit.",
    "Extreme View (EV)": "Thomson 3.0: Abortion is ALWAYS impermissible.",
    "Slightly Less Extreme View (SLEV)": "Thomson 3.1: Abortion is impermissible EXCEPT to save the mother's life AND the mother must perform it herself.",
    "Moderate Pro-life View (Mod-pro)": "Thomson 3.2: Abortion is impermissible EXCEPT to save the mother's life (a doctor may perform it).",
    "Direct Killing Argument (DKA)": "Thomson 3.0/3.1: Argues that directly killing an innocent is worse than letting someone die.",
    "Right to Life (Thomson)": "Thomson 3.2: Does NOT include the right to be given the bare minimum one needs for continued life.",
    "Moral Ownership": "Thomson 3.1: The mother morally owns her body, allowing a third party/doctor to help her.",
    "Typical vs Emergency Cases": "Thomson 3.3: Emergency = mother will die. Typical = less weighty reasons.",
    "Rights Generators 1-4": "Thomson 3.3: Suggested ways a fetus gains a right to the body. Disproved by Identical Cars.",
    "A Future Like Ours (FLO)": "Marquis: Killing is wrong because it deprives the victim of a valuable future."
}

# --- CURRICULUM WITH CHAPTER EXAMS (5 Qs Each) ---
curriculum = {
    1: {
        "title": "Chapter 1: Pogge",
        "sections": [
            {
                "subtitle": "Handout 2.2 p10-17",
                "text": "In Handout 2.2, Pogge discusses pharmaceutical testing in developing nations. He introduces the Exception to Moral Freedom: You cannot exploit desperate people for your own ends, even if you provide them with a 'net benefit' (as seen in the Eccentric Filmmaker case, where starving people are given a 50/50 chance at cash or a paint bomb). D-Lab's preferred trial is placebo-rich, but since they can't do that, they do placebo-poor in Bolivia, exploiting desperation.",
                "drill_prompt": None 
            }
        ],
        "exam": [
            {"q": "What principle does the Eccentric Filmmaker violate?", "opts": ["Moral Conditional", "Exception to Moral Freedom"], "ans": "Exception to Moral Freedom"},
            {"q": "Does providing a 'net benefit' make exploitation morally acceptable to Pogge?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Which trial type does D-Lab prefer most due to self-interest?", "opts": ["Active-rich", "Placebo-rich", "Placebo-poor"], "ans": "Placebo-rich"},
            {"q": "What is the Therapeutic Misconception?", "opts": ["Confusing a researcher for a doctor", "Confusing active drugs for placebos"], "ans": "Confusing a researcher for a doctor"},
            {"q": "Why did D-Lab run a placebo-poor trial in Bolivia?", "opts": ["It was morally best", "They couldn't run placebo-rich in the US, so they exploited looser laws abroad"], "ans": "They couldn't run placebo-rich in the US, so they exploited looser laws abroad"}
        ]
    },
    2: {
        "title": "Chapter 2: Handout 3.0 (Cuts.marked)",
        "sections": [
            {
                "subtitle": "RtL, Violinist, EV, and DKA",
                "text": "The Basic Right to Life (RtL) Argument assumes the fetus is a person with a right to life, concluding abortion is impermissible. Thomson attacks this with the Basic Violinist Case. He has a right to life, but that does NOT mean he has a right to use your kidneys. \nThe Extreme View (EV) claims abortion is ALWAYS impermissible. The Direct Killing Argument (DKA) supports this, using the technical definition that 'direct killing' is killing as an end or a means.",
                "drill_prompt": "What 2-word phrase describes the view that abortion is ALWAYS impermissible?", "drill_ans": ["extreme view", "ev"], "drill_exact": "Extreme View (EV)"
            }
        ],
        "exam": [
            {"q": "What is the primary purpose of the Basic Violinist Case?", "opts": ["To prove fetuses aren't persons", "To show a right to life does not guarantee use of a body"], "ans": "To show a right to life does not guarantee use of a body"},
            {"q": "What does the Extreme View claim about emergency abortions?", "opts": ["Always impermissible", "Permissible to save life"], "ans": "Always impermissible"},
            {"q": "How does Thomson define 'direct killing'?", "opts": ["Killing by accident", "Killing as an end in itself, or as a means to some end"], "ans": "Killing as an end in itself, or as a means to some end"},
            {"q": "Does Thomson believe the Right to Life includes the bare minimum needed to survive (like kidneys)?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "What is the core claim of the Direct Killing Argument (DKA)?", "opts": ["Direct killing is worse than letting die", "Letting die is worse than direct killing"], "ans": "Direct killing is worse than letting die"}
        ]
    },
    3: {
        "title": "Chapter 3: Handout 3.1",
        "sections": [
            {
                "subtitle": "Counterexamples, Bus Case, SLEV, Moral Ownership",
                "text": "Thomson uses counterexamples against the DKA (specifically Premise 6.4, which says you must let yourself die rather than directly kill). The Chet & Abilene (Bus) Case shows you CAN push an innocent crushing person off you. Esmerelda shows you don't have a duty to let yourself die. \nThe Slightly Less Extreme View (SLEV) says only the mother can abort to save her life. Thomson attacks SLEV using 'Moral Ownership'—the mother owns her body, so she can authorize a doctor to help her.",
                "drill_prompt": "What case attacks the duty to let yourself die using a crushing passenger?", "drill_ans": ["bus case", "chet and abilene"], "drill_exact": "The Bus Case"
            }
        ],
        "exam": [
            {"q": "What does the Bus Case attack?", "opts": ["Premise 6.4 of the DKA", "The Extreme View"], "ans": "Premise 6.4 of the DKA"},
            {"q": "Under SLEV, can a doctor perform an abortion?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "What concept allows a mother to authorize a doctor's help?", "opts": ["Therapeutic Misconception", "Moral Ownership"], "ans": "Moral Ownership"},
            {"q": "In the Bus case, is the crushing passenger considered innocent?", "opts": ["Yes", "No"], "ans": "Yes"},
            {"q": "Does Esmerelda have a duty to let herself die?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    4: {
        "title": "Chapter 4: Mod-pro View & Thomson's Rights",
        "sections": [
            {
                "subtitle": "Mod-pro, 2nd RtL, and Thomson's Rights",
                "text": "The Moderate Pro-life View (Mod-pro) claims abortion is impermissible EXCEPT to save the mother's life (a doctor MAY perform it). The 2nd version of the RtL Argument states: A fetus' right to life trumps considerations... with the possible exception of the mother's right to life. \nThomson states the Right to Life does NOT include the right to the bare minimum one needs for continued life.",
                "drill_prompt": "What view allows a doctor to perform a life-saving abortion? (Mod-___)", "drill_ans": ["mod pro", "mod-pro"], "drill_exact": "Mod-pro"
            }
        ],
        "exam": [
            {"q": "What does Mod-pro allow that SLEV does not?", "opts": ["Abortion for typical cases", "A doctor to perform the emergency abortion"], "ans": "A doctor to perform the emergency abortion"},
            {"q": "In the 2nd RtL Argument, what is the one possible exception to the fetus's right to life?", "opts": ["The mother's bodily autonomy", "The mother's right to life"], "ans": "The mother's right to life"},
            {"q": "According to Thomson, what is the actual definition of the Right to Life?", "opts": ["Right to whatever is needed to survive", "Right not to be killed unjustly"], "ans": "Right not to be killed unjustly"},
            {"q": "Does the 2nd RtL Argument allow abortion for Typical cases?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Under Mod-pro, if the mother's life is not in danger, is abortion permissible?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    5: {
        "title": "Chapter 5: Permissibility & Typical Cases",
        "sections": [
            {
                "subtitle": "Typical Cases, Large Sacrifice, & Rights Generators",
                "text": "Emergency Cases = mother will die. Typical Cases = less weighty reasons. Thomson argues if the mother must make a 'large sacrifice', and the fetus has no right to demand it, she is not morally required to do so. \nRights generators #1-4 claim intercourse grants the fetus rights. Thomson disproves this with the Identical Cars (VIP Honda Civic) case: An innocent arrival doesn't grant property rights.",
                "drill_prompt": "What do we call a scenario that disproves a rule (like the Identical Cars case)?", "drill_ans": ["counterexample", "counter example"], "drill_exact": "Counterexample"
            }
        ],
        "exam": [
            {"q": "What defines a 'Typical Case'?", "opts": ["Life or death", "Less weighty reasons than preserving life"], "ans": "Less weighty reasons than preserving life"},
            {"q": "What does Thomson's argument for permissibility rely on?", "opts": ["The mother not having to make a 'large sacrifice'", "The fetus not being a person"], "ans": "The mother not having to make a 'large sacrifice'"},
            {"q": "What case disproves Rights Generators 1-4?", "opts": ["Identical Cars (Honda Civic)", "The Bus Case"], "ans": "Identical Cars (Honda Civic)"},
            {"q": "Does an innocent arrival in your car grant them a moral right to it?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Do Rights Generators 1-4 successfully prove a fetus has a right to the mother's body?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    6: {
        "title": "Chapter 6: Logic, Validity & Soundness",
        "sections": [
            {
                "subtitle": "Validity, Soundness, and Conditionals",
                "text": "To test for validity: suppose all premises are true. If it's possible for the conclusion to be false, it is INVALID. Soundness means it is VALID and all premises are ACTUALLY true. \nConditional = 'If X, then Y'. Antecedent = the 'If' part. Consequent = the 'Then' part.",
                "drill_prompt": "What is an argument that is valid AND has all true premises called?", "drill_ans": ["sound", "soundness"], "drill_exact": "Sound"
            }
        ],
        "exam": [
            {"q": "How do you test for Validity?", "opts": ["Suppose premises true, see if conclusion can be false", "Check if premises are actually true"], "ans": "Suppose premises true, see if conclusion can be false"},
            {"q": "What is Soundness?", "opts": ["Valid + True premises", "Invalid + True premises"], "ans": "Valid + True premises"},
            {"q": "What is the 'antecedent'?", "opts": ["The 'If' part", "The 'Then' part"], "ans": "The 'If' part"},
            {"q": "What is the 'consequent'?", "opts": ["The 'If' part", "The 'Then' part"], "ans": "The 'Then' part"},
            {"q": "If an argument is valid but a premise is false in reality, is it sound?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    7: {
        "title": "Chapter 7: The Basic Right to Life Argument",
        "sections": [
            {
                "subtitle": "The Basic Right to Life Argument",
                "text": "1. Fetus is a person.\n2. Every person has a right to life.\n3. Fetus has a right to life.\n4. A person's right to life trumps bodily rights and makes killing impermissible.\n5. Abortion kills fetus.\nC: Abortion is impermissible.",
                "drill_prompt": "Which premise claims the right to life trumps bodily rights?", "drill_ans": ["4", "premise 4"], "drill_exact": "Premise 4"
            }
        ],
        "exam": [
            {"q": "What does Premise 1 assume?", "opts": ["Fetus is a person", "Fetus is a cluster of cells"], "ans": "Fetus is a person"},
            {"q": "What does Premise 4 explicitly claim?", "opts": ["Right to life trumps bodily rights", "Bodily autonomy trumps right to life"], "ans": "Right to life trumps bodily rights"},
            {"q": "What is the conclusion of this argument?", "opts": ["Abortion is permissible", "Abortion is impermissible"], "ans": "Abortion is impermissible"},
            {"q": "Does Thomson agree with Premise 4?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "What does Premise 2 claim?", "opts": ["Every person has a right to life", "Fetuses aren't persons"], "ans": "Every person has a right to life"}
        ]
    },
    8: {
        "title": "Chapter 8: Basic RtL Applied to the Violinist",
        "sections": [
            {
                "subtitle": "Basic RtL Argument, Applied to the Violinist",
                "text": "1. Violinist is a person. 2. Persons have RtL. 3. Violinist has RtL. 4. RtL trumps bodily rights. 5. Unhooking kills violinist. C: Impermissible to unhook yourself.\nBecause the conclusion is absurd (you CAN unhook), Thomson proves Premise 4 is false.",
                "drill_prompt": "If the conclusion is false, the argument cannot be _______.", "drill_ans": ["sound"], "drill_exact": "Sound"
            }
        ],
        "exam": [
            {"q": "What is the conclusion of this applied argument?", "opts": ["You can unhook", "It is impermissible to unhook"], "ans": "It is impermissible to unhook"},
            {"q": "What is Thomson's view of this conclusion?", "opts": ["It is true", "It is absurd/false"], "ans": "It is absurd/false"},
            {"q": "Because the conclusion is false, what happens to Premise 4?", "opts": ["It is proven true", "It is proven false"], "ans": "It is proven false"},
            {"q": "In this argument, does the Violinist have a Right to Life?", "opts": ["Yes", "No"], "ans": "Yes"},
            {"q": "Does unhooking kill the violinist according to Premise 5?", "opts": ["Yes", "No"], "ans": "Yes"}
        ]
    },
    9: {
        "title": "Chapter 9: The Direct Killing Argument",
        "sections": [
            {
                "subtitle": "The Direct Killing Argument",
                "text": "2. Abortion is direct killing. 3. Fetus is innocent. 5. Not aborting is letting mother die. 6.4: If options are direct killing vs letting die, you must prefer letting die. C: Impermissible to abort.",
                "drill_prompt": "What is the 3-letter abbreviation for the Direct Killing Argument?", "drill_ans": ["dka"], "drill_exact": "DKA"
            }
        ],
        "exam": [
            {"q": "What does Premise 2 claim abortion is?", "opts": ["Direct killing", "Letting die"], "ans": "Direct killing"},
            {"q": "What does Premise 5 claim not aborting is?", "opts": ["Direct killing", "Letting the mother die"], "ans": "Letting the mother die"},
            {"q": "What does Premise 6.4 demand you prefer?", "opts": ["Letting die", "Direct killing"], "ans": "Letting die"},
            {"q": "What does Premise 6.2 claim direct killing is?", "opts": ["Murder", "Self-defense"], "ans": "Murder"},
            {"q": "What is the conclusion of the DKA?", "opts": ["Impermissible even to save the mother", "Permissible to save the mother"], "ans": "Impermissible even to save the mother"}
        ]
    },
    10: {
        "title": "Chapter 10: DKA v6.2 Applied to the Violinist",
        "sections": [
            {
                "subtitle": "DKA v6.2 Applied to the Violinist",
                "text": "2. Unhooking is direct killing. 5. Not unhooking is letting yourself die. 6.2: Direct killing an innocent is murder, which is absolutely impermissible. C: Impermissible to unhook, even to save your life.",
                "drill_prompt": "Does Thomson believe you must stay hooked up to save your life?", "drill_ans": ["no", "false"], "drill_exact": "No"
            }
        ],
        "exam": [
            {"q": "What does Premise 6.2 claim direct killing is?", "opts": ["Murder", "Accident"], "ans": "Murder"},
            {"q": "How is unhooking framed in Premise 2?", "opts": ["Letting die", "Direct killing"], "ans": "Direct killing"},
            {"q": "What is the conclusion of this argument?", "opts": ["Impermissible to unhook", "Permissible to unhook"], "ans": "Impermissible to unhook"},
            {"q": "What is Thomson's reaction to this conclusion?", "opts": ["It is true", "It is false, you can unhook"], "ans": "It is false, you can unhook"},
            {"q": "What does this mean for Premise 6.2?", "opts": ["It is perfectly sound", "It is flawed in this context"], "ans": "It is flawed in this context"}
        ]
    },
    11: {
        "title": "Chapter 11: DKA Applied to the Bus Case",
        "sections": [
            {
                "subtitle": "DKA Applied to the Bus Case",
                "text": "2. Pushing the crushing passenger off is direct killing. 5. Not pushing is letting yourself die. C: Impermissible to push them off. Thomson shows this is absurd; you CAN push an innocent threat off.",
                "drill_prompt": "Who is crushing Chet in the Bus Case?", "drill_ans": ["abilene"], "drill_exact": "Abilene"
            }
        ],
        "exam": [
            {"q": "Who is crushing Chet?", "opts": ["Abilene", "Esmerelda"], "ans": "Abilene"},
            {"q": "What is pushing her off classified as in the argument?", "opts": ["Direct killing an innocent", "Letting die"], "ans": "Direct killing an innocent"},
            {"q": "What is letting her crush you classified as?", "opts": ["Letting yourself die", "Murder"], "ans": "Letting yourself die"},
            {"q": "What is the DKA conclusion here?", "opts": ["Impermissible to push her", "Permissible to push her"], "ans": "Impermissible to push her"},
            {"q": "What is Thomson's reaction to this conclusion?", "opts": ["Absurd, you can push her off", "True, you must die"], "ans": "Absurd, you can push her off"}
        ]
    },
    12: {
        "title": "Chapter 12: The 2nd Version of the RtL Argument",
        "sections": [
            {
                "subtitle": "The Second Version of the Right to Life Argument",
                "text": "4. A fetus' right to life trumps all considerations, with the possible exception of the mother's right to life. C: If a woman does not need an abortion to save her life, it is impermissible.",
                "drill_prompt": "This argument perfectly aligns with which Pro-Life view? (Mod-___)", "drill_ans": ["mod pro", "mod-pro"], "drill_exact": "Mod-pro"
            }
        ],
        "exam": [
            {"q": "What is the ONLY exception to the fetus's right to life in Premise 4?", "opts": ["The mother's right to life", "Bodily autonomy"], "ans": "The mother's right to life"},
            {"q": "If the mother's life is not in danger, what is the conclusion?", "opts": ["Permissible", "Impermissible"], "ans": "Impermissible"},
            {"q": "Which Pro-life view does this align with?", "opts": ["SLEV", "Mod-pro"], "ans": "Mod-pro"},
            {"q": "Does this argument allow abortion for Typical cases?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Does Thomson ultimately accept this argument?", "opts": ["Yes", "No, she attacks it with the Large Sacrifice argument"], "ans": "No, she attacks it with the Large Sacrifice argument"}
        ]
    }
}

# --- MASTER FINAL EXAM BANK (20 Random Qs) ---
exam_bank = [
    {"q": "How do you test for Validity?", "opts": ["See if premises are true in reality.", "Suppose premises are true, see if conclusion can be false."], "ans": "Suppose premises are true, see if conclusion can be false.", "exp": "Validity only tests logical structure."},
    {"q": "What is Soundness?", "opts": ["Valid + All premises are true.", "Invalid + True premises."], "ans": "Valid + All premises are true.", "exp": "Must be valid AND have true premises."},
    {"q": "What is the 'antecedent' of a conditional?", "opts": ["The 'Then' part.", "The 'If' part."], "ans": "The 'If' part.", "exp": "Antecedent comes first (If)."},
    {"q": "What does the Extreme View (EV) say about emergency abortions?", "opts": ["Permissible if mother does it.", "Always impermissible."], "ans": "Always impermissible.", "exp": "EV allows zero exceptions."},
    {"q": "What does SLEV say about emergency abortions?", "opts": ["Only the mother herself may perform it to save her life.", "A doctor may perform it."], "ans": "Only the mother herself may perform it to save her life.", "exp": "SLEV forbids third-party intervention."},
    {"q": "What concept does Thomson use to argue against SLEV?", "opts": ["Moral Ownership", "Exception to Moral Freedom"], "ans": "Moral Ownership", "exp": "The mother morally owns her body and can authorize a doctor."},
    {"q": "What does Mod-pro allow?", "opts": ["Abortion only to save mother's life (doctor permitted).", "Abortion only if mother performs it."], "ans": "Abortion only to save mother's life (doctor permitted).", "exp": "Mod-pro allows doctor intervention."},
    {"q": "What does Premise 6.4 of the DKA state?", "opts": ["Killing is murder.", "Must prefer letting die over direct killing."], "ans": "Must prefer letting die over direct killing.", "exp": "6.4 forces the 'let die' option."},
    {"q": "What case counteracts Premise 6.4?", "opts": ["Eccentric Filmmaker", "Chet & Abilene (Bus) Case"], "ans": "Chet & Abilene (Bus) Case", "exp": "Shows you ARE allowed to directly kill an innocent threat."},
    {"q": "Thomson's definition of 'Direct Killing'?", "opts": ["Killing by accident.", "Killing as an end in itself, or as a means to some end."], "ans": "Killing as an end in itself, or as a means to some end.", "exp": "Exact definition from footnote 3."},
    {"q": "Does the Right to Life include the right to the bare minimum needed for life?", "opts": ["Yes.", "No."], "ans": "No.", "exp": "Right to life doesn't guarantee another's kidneys."},
    {"q": "What defines a 'Typical Case'?", "opts": ["Life or death.", "Less weighty reason than preserving own life."], "ans": "Less weighty reason than preserving own life.", "exp": "Typical cases contrast with emergencies."},
    {"q": "What case disproves Rights Generators 1-4?", "opts": ["Identical Cars (Honda Civic)", "Violinist"], "ans": "Identical Cars (Honda Civic)", "exp": "Innocent arrival doesn't grant property rights."},
    {"q": "Does providing a net benefit excuse exploitation according to Pogge?", "opts": ["Yes.", "No."], "ans": "No.", "exp": "Exception to Moral Freedom proves it's still grotesque."},
    {"q": "In the 2nd Version of the RtL Argument, what is the ONLY exception?", "opts": ["Mother's bodily autonomy.", "Mother's right to life."], "ans": "Mother's right to life.", "exp": "Premise 4 explicitly notes this."},
    {"q": "What is the purpose of the Violinist Case?", "opts": ["Prove fetuses aren't human.", "Prove Right to Life doesn't guarantee use of another's body."], "ans": "Prove Right to Life doesn't guarantee use of another's body.", "exp": "Attacks the Basic RtL Argument."},
    {"q": "If valid but premises are false in reality, the argument is:", "opts": ["Sound", "Unsound"], "ans": "Unsound", "exp": "Soundness requires validity AND true premises."},
    {"q": "Pogge's Exception to Moral Freedom case?", "opts": ["Eccentric Filmmaker", "Bus Case"], "ans": "Eccentric Filmmaker", "exp": "Exploits desperate people for a game."},
    {"q": "Is 'If it rains, then ground gets wet' a conditional?", "opts": ["Yes", "No"], "ans": "Yes", "exp": "Conditionals are 'If/Then'."},
    {"q": "Consequent of 'If I study, then I will pass'?", "opts": ["If I study", "I will pass"], "ans": "I will pass", "exp": "Consequent is the 'Then' portion."},
    {"q": "Is the crushing person in the Bus Case innocent?", "opts": ["Yes", "No"], "ans": "Yes", "exp": "They didn't intend to fall on you."},
    {"q": "What does DKA stand for?", "opts": ["Direct Killing Argument", "Duty to Keep Alive"], "ans": "Direct Killing Argument", "exp": "Major focus of Handouts 3.0/3.1."},
    {"q": "According to Marquis, why is killing wrong?", "opts": ["Deprives victim of a Future Like Ours", "Violates bodily autonomy"], "ans": "Deprives victim of a Future Like Ours", "exp": "A Future Like Ours (FLO) argument."}
]

# --- SESSION STATE ---
def init_state():
    if 'current_ch' not in st.session_state: st.session_state.current_ch = 1
    if 'current_sec' not in st.session_state: st.session_state.current_sec = 0
    if 'drill_state' not in st.session_state: st.session_state.drill_state = "unanswered"
    if 'redo_queue' not in st.session_state: st.session_state.redo_queue = []
    
    # Chapter Exam State
    if 'in_chapter_exam' not in st.session_state: st.session_state.in_chapter_exam = False
    if 'ch_exam_q_index' not in st.session_state: st.session_state.ch_exam_q_index = 0
    if 'ch_exam_failed' not in st.session_state: st.session_state.ch_exam_failed = False

    # Final Exam State
    if 'exam_q_index' not in st.session_state: st.session_state.exam_q_index = 0
    if 'exam_pool' not in st.session_state: st.session_state.exam_pool = []
    if 'exam_q_passed' not in st.session_state: st.session_state.exam_q_passed = False

init_state()

def check_spelling(user_input, valid_phrases):
    clean_in = re.sub(r'[^\w\s]', '', user_input).lower().strip()
    return any(re.sub(r'[^\w\s]', '', p).lower().strip() == clean_in for p in valid_phrases)

def advance_section():
    ch = st.session_state.current_ch
    sec = st.session_state.current_sec
    
    if sec + 1 < len(curriculum[ch]["sections"]):
        st.session_state.current_sec += 1
        st.session_state.drill_state = "unanswered"
    else:
        # Move to Chapter Exam
        st.session_state.in_chapter_exam = True
        st.session_state.ch_exam_q_index = 0
        st.session_state.ch_exam_failed = False

# --- SIDEBAR: TABLE OF CONTENTS ---
st.sidebar.markdown("### 📖 Table of Contents")
for i in range(1, 13):
    if st.session_state.current_ch == i:
        st.sidebar.markdown(f"**👉 Chapter {i}: {curriculum[i]['title'].split(':')[1].strip()}**")
    else:
        st.sidebar.markdown(f"Chapter {i}")

if st.session_state.current_ch == 13: st.sidebar.markdown("**👉 Redo Gauntlet**")
else: st.sidebar.markdown("Redo Gauntlet")

if st.session_state.current_ch == 14: st.sidebar.markdown("**👉 Final Exam**")
else: st.sidebar.markdown("Final Exam")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Vocab Dictionary")
for word, defi in vocab_defs.items():
    with st.sidebar.expander(f"📖 {word}"):
        st.write(defi)

if st.sidebar.button("Restart Completely 🔄"):
    st.session_state.clear()
    init_state()
    st.rerun()

# --- MAIN APP LOGIC ---

# CHAPTERS 1 - 12 (Learning Mode & Chapter Exams)
if st.session_state.current_ch <= 12:
    ch = st.session_state.current_ch
    ch_data = curriculum[ch]
    
    st.title(ch_data["title"])
    
    # NORMAL READING / DRILL MODE
    if not st.session_state.in_chapter_exam:
        sec_data = ch_data["sections"][st.session_state.current_sec]
        st.subheader(sec_data["subtitle"])
        st.markdown(f"<div class='story-box'>{sec_data['text'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        
        if sec_data["drill_prompt"]:
            st.markdown(f"<div class='drill-box'><b>✏️ Drill:</b> {sec_data['drill_prompt']}</div>", unsafe_allow_html=True)
            ans = st.text_input("Type answer:", key="drill_input")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Submit Drill"):
                    if check_spelling(ans, sec_data["drill_ans"]): st.session_state.drill_state = "correct"
                    else:
                        st.session_state.drill_state = "wrong"
                        if not any(d["prompt"] == sec_data["drill_prompt"] for d in st.session_state.redo_queue):
                            st.session_state.redo_queue.append({"prompt": sec_data["drill_prompt"], "valid": sec_data["drill_ans"], "exact": sec_data["drill_exact"]})
            with c2:
                if st.button("Show Answer"):
                    st.session_state.drill_state = "show"
                    if not any(d["prompt"] == sec_data["drill_prompt"] for d in st.session_state.redo_queue):
                        st.session_state.redo_queue.append({"prompt": sec_data["drill_prompt"], "valid": sec_data["drill_ans"], "exact": sec_data["drill_exact"]})
            
            if st.session_state.drill_state == "correct":
                st.success("✅ Perfect!")
                if st.button("Proceed ➡️"):
                    advance_section()
                    st.rerun()
            elif st.session_state.drill_state == "wrong": st.error("❌ Not quite. Try again or 'Show Answer'.")
            elif st.session_state.drill_state == "show":
                st.info(f"Answer: **{sec_data['drill_exact']}** (Added to Gauntlet)")
                if st.button("Acknowledge & Proceed ➡️"):
                    advance_section()
                    st.rerun()
        else:
            if st.button("Proceed ➡️"):
                advance_section()
                st.rerun()
                
    # CHAPTER EXAM MODE
    else:
        st.markdown("<div class='exam-box'><h3>📝 Chapter Mastery Exam</h3>You must score 5/5 to proceed to the next chapter. A single mistake will force a chapter restart!</div>", unsafe_allow_html=True)
        
        if st.session_state.ch_exam_failed:
            st.error("❌ You missed a question! You must achieve 100% mastery. Restarting chapter...")
            if st.button("Restart Chapter Reading 🔄"):
                st.session_state.current_sec = 0
                st.session_state.in_chapter_exam = False
                st.session_state.ch_exam_failed = False
                st.session_state.drill_state = "unanswered"
                st.rerun()
                
        elif st.session_state.ch_exam_q_index >= 5:
            st.balloons()
            st.success("🎉 5/5! You mastered this chapter.")
            if st.button("Start Next Chapter ➡️"):
                st.session_state.current_ch += 1
                st.session_state.current_sec = 0
                st.session_state.in_chapter_exam = False
                st.session_state.drill_state = "unanswered"
                st.rerun()
                
        else:
            q_data = ch_data["exam"][st.session_state.ch_exam_q_index]
            st.write(f"**Question {st.session_state.ch_exam_q_index + 1} of 5:** {q_data['q']}")
            for opt in q_data["opts"]:
                if st.button(opt):
                    if opt == q_data["ans"]:
                        st.session_state.ch_exam_q_index += 1
                        st.rerun()
                    else:
                        st.session_state.ch_exam_failed = True
                        st.rerun()

# STAGE 13: REDO GAUNTLET
elif st.session_state.current_ch == 13:
    st.title("🧠 The Redo Gauntlet")
    if len(st.session_state.redo_queue) == 0:
        st.success("🎉 Gauntlet cleared! You are ready for the Final Exam.")
        if st.button("Start Final Exam 📝"):
            st.session_state.current_ch = 14
            st.rerun()
    else:
        st.warning(f"{len(st.session_state.redo_queue)} questions to review before the exam.")
        curr = st.session_state.redo_queue[0]
        st.write(f"**✏️ Re-Test:** {curr['prompt']}")
        redo_ans = st.text_input("Type exact answer:")
        if st.button("Submit"):
            if check_spelling(redo_ans, curr["valid"]):
                st.success("✅ Got it!")
                st.session_state.redo_queue.pop(0)
                st.button("Next", on_click=lambda: st.rerun())
            else:
                st.error(f"❌ Still incorrect. Answer is **{curr['exact']}**")

# STAGE 14: FINAL EXAM
elif st.session_state.current_ch == 14:
    st.title("📝 Comprehensive Final Exam")
    st.write("20 randomly selected questions based directly on course notes. You must get each correct to proceed.")
    
    if not st.session_state.exam_pool:
        st.session_state.exam_pool = random.sample(exam_bank, 20)
        
    if st.session_state.exam_q_index >= 20:
        st.balloons()
        st.success("🎉 YOU PASSED THE FINAL EXAM! You are officially prepared to teach this material to someone else.")
        if st.button("Restart App"):
            st.session_state.clear()
            init_state()
            st.rerun()
    else:
        q_data = st.session_state.exam_pool[st.session_state.exam_q_index]
        st.markdown(f"### Question {st.session_state.exam_q_index + 1} of 20")
        st.write(q_data["q"])
        
        if not st.session_state.exam_q_passed:
            for opt in q_data["opts"]:
                if st.button(opt):
                    if opt == q_data["ans"]:
                        st.session_state.exam_q_passed = True
                        st.rerun()
                    else:
                        st.error(f"❌ Incorrect. **Why?** {q_data['exp']}")
        else:
            st.success(f"✅ Correct! {q_data['exp']}")
            if st.button("Next Question ➡️"):
                st.session_state.exam_q_index += 1
                st.session_state.exam_q_passed = False
                st.rerun()
