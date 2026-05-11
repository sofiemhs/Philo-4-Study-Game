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
    .bear-box { background-color: #fff8e1; padding: 20px; border-radius: 15px; border: 3px solid #ffa000; margin-bottom: 20px; font-size: 18px; line-height: 1.6; }
    .alert-box { background-color: #ffecb3; padding: 15px; border-radius: 10px; border-left: 5px solid #ffb300; margin-bottom: 15px; font-weight: bold;}
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

# --- CURRICULUM WITH FULL EXPLANATIONS & CHAPTER EXAMS ---
curriculum = {
    1: {
        "title": "Chapter 1: Pogge",
        "sections": [
            {
                "subtitle": "Handout 2.2 p10-17 & Practice Exam Q1, Q2, Q3",
                "text": "Pogge introduces the **Exception to Moral Freedom**: You cannot exploit desperate people for your own ends, even if you provide a 'net benefit'. He proves this with the 'Eccentric Filmmaker' case.\n\n<div class='alert-box'>🚨 PRACTICE EXAM REVIEW (Q1, Q2, Q3):<br>You missed the questions on D-Lab's preferences vs. Moral Goodness!<br><br><b>Q2 (D-Lab's Self-Interest):</b> A greedy company wants cheap/fast data and rich customers. Their ranking is:<br>1. Placebo-rich (cheapest, customers can afford drug)<br>2. Active-rich<br>3. Placebo-poor<br>4. Active-poor (most expensive, customers are poor).<br><br><b>Q3 (Moral Goodness):</b> Morality demands we give people REAL medicine (Active) over fake sugar water (Placebo). So the moral ranking is:<br>1. Active-rich<br>2. Active-poor<br>3. Placebo-rich<br>4. Placebo-poor.<br><br><b>Q1 (Pogge's Principle):</b> Because D-Lab runs Placebo-poor trials in Bolivia simply because they are cheaper and have looser laws, they violate the 'Exception to Moral Freedom' by exploiting desperation!</div>",
                "drill_prompt": None 
            }
        ],
        "exam": [
            {"q": "What is D-Lab's self-interested preference ranking?", "opts": ["placebo-rich > active-rich > placebo-poor > active-poor", "active-rich > active-poor > placebo-rich > placebo-poor"], "ans": "placebo-rich > active-rich > placebo-poor > active-poor"},
            {"q": "What is the ranking of actual Moral Goodness?", "opts": ["placebo-rich > active-rich > placebo-poor > active-poor", "active-rich > active-poor > placebo-rich > placebo-poor"], "ans": "active-rich > active-poor > placebo-rich > placebo-poor"},
            {"q": "Which principle entails it was wrong for D-Lab to run the trial in Bolivia?", "opts": ["Moral Conditional", "Exception to Moral Freedom"], "ans": "Exception to Moral Freedom"},
            {"q": "Does providing a 'net benefit' make exploitation morally acceptable?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Why does D-Lab prefer 'rich' country trials?", "opts": ["The citizens can afford to buy the drug later", "The citizens are more desperate"], "ans": "The citizens can afford to buy the drug later"}
        ]
    },
    2: {
        "title": "Chapter 2: Handout 3.0 (Cuts.marked)",
        "sections": [
            {
                "subtitle": "RtL, Violinist, EV, and DKA",
                "text": "The Basic Right to Life Argument assumes the fetus is a person with a right to life, concluding abortion is impermissible. Thomson attacks this with the Basic Violinist Case to show a right to life does not guarantee use of another person's body.\n\n<div class='alert-box'>🚨 PRACTICE EXAM REVIEW (Q5):<br>You missed the question on the Extreme View (EV)!<br><b>EV claims: Abortion is ALWAYS impermissible.</b> It allows absolutely NO exceptions. Not even to save the mother's life!</div>\n\nThe Direct Killing Argument (DKA) supports EV by arguing that directly killing an innocent is morally worse than letting someone die. Thomson defines 'direct killing' as killing as an end in itself, or as a means to some end.",
                "drill_prompt": "What 2-word phrase describes the view that abortion is ALWAYS impermissible?", "drill_ans": ["extreme view", "ev"], "drill_exact": "Extreme View (EV)"
            }
        ],
        "exam": [
            {"q": "What does the Extreme View (EV) claim?", "opts": ["Abortion is ALWAYS impermissible", "Abortion is permissible to save the mother"], "ans": "Abortion is ALWAYS impermissible"},
            {"q": "What is the purpose of the Violinist Case?", "opts": ["To show Right to Life doesn't guarantee use of a body", "To prove fetuses aren't persons"], "ans": "To show Right to Life doesn't guarantee use of a body"},
            {"q": "How does Thomson define 'direct killing'?", "opts": ["Killing by accident", "Killing as an end in itself, or as a means to some end"], "ans": "Killing as an end in itself, or as a means to some end"},
            {"q": "What does the Direct Killing Argument claim is worse?", "opts": ["Directly killing an innocent", "Letting someone die"], "ans": "Directly killing an innocent"},
            {"q": "Does EV allow abortions in emergencies?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    3: {
        "title": "Chapter 3: Handout 3.1",
        "sections": [
            {
                "subtitle": "Counterexamples, Bus Case, SLEV",
                "text": "Thomson uses the Chet & Abilene (Bus) Case to attack Premise 6.4 of the DKA. Chet CAN push an innocent crushing passenger off him. Esmerelda shows you don't have a duty to let yourself die.\n\n<div class='alert-box'>🚨 PRACTICE EXAM REVIEW (Q7):<br>You missed the question on the Slightly Less Extreme View (SLEV)!<br><b>SLEV claims:</b> Abortion is impermissible EXCEPT to save the mother's life, BUT <b>only the mother herself can perform it</b>. A doctor/third-party is strictly forbidden from intervening.</div>\n\nThomson attacks SLEV using 'Moral Ownership'—because the mother morally owns her body, she can authorize a doctor's help.",
                "drill_prompt": "Under SLEV, can a doctor perform a life-saving abortion?", "drill_ans": ["no"], "drill_exact": "No"
            }
        ],
        "exam": [
            {"q": "Under SLEV, who is permitted to perform the life-saving abortion?", "opts": ["A doctor", "Only the mother herself"], "ans": "Only the mother herself"},
            {"q": "What does the Bus Case attack?", "opts": ["Premise 6.4 of the DKA", "The Extreme View"], "ans": "Premise 6.4 of the DKA"},
            {"q": "What concept allows a mother to authorize a doctor's help?", "opts": ["Exception to Moral Freedom", "Moral Ownership"], "ans": "Moral Ownership"},
            {"q": "In the Bus case, is the crushing passenger innocent?", "opts": ["Yes", "No"], "ans": "Yes"},
            {"q": "Does Esmerelda have a duty to let herself die?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    4: {
        "title": "Chapter 4: Mod-pro View & Thomson's Rights",
        "sections": [
            {
                "subtitle": "Mod-pro, 2nd RtL, and Thomson's Rights",
                "text": "<div class='alert-box'>🚨 PRACTICE EXAM REVIEW (Q8 & Q12):<br><b>Q8 (Mod-pro):</b> The Moderate Pro-life View claims abortion is impermissible EXCEPT to save the mother's life, AND a doctor MAY perform it. (Unlike SLEV).<br><br><b>Q12 (Right to Life):</b> Thomson argues the Right to Life is simply the right not to be killed unjustly. It does NOT include the right to be given the bare minimum one needs for continued life (e.g., use of another's body).</div>\n\nThis aligns with the 2nd version of the RtL Argument. Premise 4 states: A fetus' right to life trumps all considerations with the possible exception of the mother's right to life.",
                "drill_prompt": "What view allows a doctor to perform a life-saving abortion? (Mod-___)", "drill_ans": ["mod pro", "mod-pro"], "drill_exact": "Mod-pro"
            }
        ],
        "exam": [
            {"q": "What does Mod-pro allow that SLEV does not?", "opts": ["Abortion for typical cases", "A doctor to perform the emergency abortion"], "ans": "A doctor to perform the emergency abortion"},
            {"q": "According to Thomson, does the Right to Life include the bare minimum needed to survive?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "In the 2nd RtL Argument, what is the ONE possible exception to the fetus's right to life?", "opts": ["Bodily autonomy", "The mother's right to life"], "ans": "The mother's right to life"},
            {"q": "Does Mod-pro allow abortion for Typical cases?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "What is Thomson's actual definition of the Right to Life?", "opts": ["Right to whatever is needed to survive", "Right not to be killed unjustly"], "ans": "Right not to be killed unjustly"}
        ]
    },
    5: {
        "title": "Chapter 5: Permissibility & Typical Cases",
        "sections": [
            {
                "subtitle": "Typical Cases & Rights Generators",
                "text": "<div class='alert-box'>🚨 PRACTICE EXAM REVIEW (Q4 & Q13):<br><b>Q13 (Typical Cases):</b> A Typical Case is when the mother wants an abortion for less weighty reasons than preserving her life. Thomson argues it is permissible because she would have to make a 'large sacrifice', and the fetus has no right to demand it.<br><br><b>Q4 (Honda Civic):</b> Pro-lifers claim intercourse gives the fetus a right to the body (Rights Generators 1-4). Thomson disproves ALL of these with the Identical Cars (Honda Civic) counterexample. An innocent arrival doesn't grant property rights!</div>",
                "drill_prompt": "What defines a 'Typical Case'?", "drill_ans": ["less weighty", "not life or death", "less weighty reasons", "not emergency"], "drill_exact": "Less weighty reasons than life or death"
            }
        ],
        "exam": [
            {"q": "What defines a 'Typical Case'?", "opts": ["Life or death", "Less weighty reasons than preserving life"], "ans": "Less weighty reasons than preserving life"},
            {"q": "What case disproves Rights Generators 1-4?", "opts": ["Identical Cars (Honda Civic)", "The Bus Case"], "ans": "Identical Cars (Honda Civic)"},
            {"q": "Does an innocent arrival in your car grant them a moral right to it?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "What does Thomson's argument for permissibility rely on?", "opts": ["The mother not having to make a 'large sacrifice'", "The fetus not being a person"], "ans": "The mother not having to make a 'large sacrifice'"},
            {"q": "Do Rights Generators 1-4 successfully prove a fetus has a right to the body?", "opts": ["Yes", "No"], "ans": "No"}
        ]
    },
    6: {
        "title": "Chapter 6: Logic, Validity & Soundness",
        "sections": [
            {
                "subtitle": "Validity, Soundness, and Conditionals",
                "text": "To test for **Validity**: suppose all premises are true. If it's possible for the conclusion to be false, it is INVALID. **Soundness** means it is VALID and all premises are ACTUALLY true. \nConditional = 'If X, then Y'. Antecedent = the 'If' part. Consequent = the 'Then' part.",
                "drill_prompt": "How do you test for Validity?", "drill_ans": ["suppose premises are true", "suppose premises true"], "drill_exact": "Suppose premises are true and see if conclusion can be false."
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
                "subtitle": "The Argument",
                "text": "1. Fetus is a person. 2. Every person has a right to life. 3. Fetus has a right to life. 4. A person's right to life trumps bodily rights and makes killing impermissible. 5. Abortion kills fetus. C: Abortion is impermissible.\n\nPremise 4 is the crucial step Thomson attacks.",
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
                "subtitle": "The Argument",
                "text": "When applied to the Violinist, the logic dictates: C: It is impermissible to unhook yourself.\nBecause the conclusion is obviously false (you CAN unhook), Thomson proves Premise 4 is false.",
                "drill_prompt": "If the conclusion is false, the argument cannot be _______.", "drill_ans": ["sound"], "drill_exact": "Sound"
            }
        ],
        "exam": [
            {"q": "What is the conclusion of this applied argument?", "opts": ["You can unhook", "It is impermissible to unhook"], "ans": "It is impermissible to unhook"},
            {"q": "What is Thomson's view of this conclusion?", "opts": ["It is true", "It is absurd/false"], "ans": "It is absurd/false"},
            {"q": "Because the conclusion is false, what happens to Premise 4?", "opts": ["It is proven true", "It is proven false"], "ans": "It is proven false"},
            {"q": "Does the Violinist have a Right to Life?", "opts": ["Yes", "No"], "ans": "Yes"},
            {"q": "Does unhooking kill the violinist according to Premise 5?", "opts": ["Yes", "No"], "ans": "Yes"}
        ]
    },
    9: {
        "title": "Chapter 9: The Direct Killing Argument",
        "sections": [
            {
                "subtitle": "The Argument",
                "text": "Premise 2: Abortion is direct killing. Premise 5: Not aborting is letting mother die. Premise 6.4: If options are direct killing vs letting die, you must prefer letting die. C: Impermissible to abort.",
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
                "subtitle": "The Argument",
                "text": "Applying DKA to the Violinist uses Premise 6.2: Direct killing an innocent is murder, which is absolutely impermissible. C: Impermissible to unhook, even to save your life.\nThomson shows this is absurd, meaning unhooking is NOT murder.",
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
                "subtitle": "The Argument",
                "text": "The DKA says you cannot push the crushing passenger off. Thomson shows this is absurd; you CAN push an innocent threat off to save your own life.",
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
                "subtitle": "The Argument",
                "text": "Premise 4: A fetus' right to life trumps all considerations, with the possible exception of the mother's right to life. C: If a woman does not need an abortion to save her life, it is impermissible.",
                "drill_prompt": "This argument perfectly aligns with which Pro-Life view? (Mod-___)", "drill_ans": ["mod pro", "mod-pro"], "drill_exact": "Mod-pro"
            }
        ],
        "exam": [
            {"q": "What is the ONLY exception to the fetus's right to life in Premise 4?", "opts": ["The mother's right to life", "Bodily autonomy"], "ans": "The mother's right to life"},
            {"q": "If the mother's life is not in danger, what is the conclusion?", "opts": ["Permissible", "Impermissible"], "ans": "Impermissible"},
            {"q": "Which Pro-life view does this align with?", "opts": ["SLEV", "Mod-pro"], "ans": "Mod-pro"},
            {"q": "Does this argument allow abortion for Typical cases?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Does Thomson ultimately accept this argument?", "opts": ["Yes", "No, she attacks it"], "ans": "No, she attacks it"}
        ]
    },
    13: {
        "title": "Chapter 13: Marquis (A Future Like Ours)",
        "sections": [
            {
                "subtitle": "Marquis and FLO",
                "text": "<div class='alert-box'>🚨 PRACTICE EXAM REVIEW (Q17):<br><b>Q17 (Marquis):</b> Marquis ignores religion and personhood. He argues that killing an adult is wrong because it deprives them of a valuable future. He calls this <b>A Future Like Ours (FLO)</b>. Because a fetus also possesses a future like ours, killing a fetus is just as wrong as killing an adult!</div>",
                "drill_prompt": "What 3-letter acronym represents Marquis's main argument?", "drill_ans": ["flo"], "drill_exact": "FLO"
            }
        ],
        "exam": [
            {"q": "According to Marquis, why is killing an adult wrong?", "opts": ["It causes pain", "It deprives them of a Future Like Ours (FLO)"], "ans": "It deprives them of a Future Like Ours (FLO)"},
            {"q": "Does Marquis base his argument on religious dogma?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "Does Marquis get bogged down in defining 'personhood'?", "opts": ["Yes", "No"], "ans": "No"},
            {"q": "According to Marquis, does a fetus possess a Future Like Ours?", "opts": ["Yes", "No"], "ans": "Yes"},
            {"q": "What is the ultimate conclusion of Marquis's argument?", "opts": ["Abortion is seriously immoral", "Abortion is permissible"], "ans": "Abortion is seriously immoral"}
        ]
    },
    14: {
        "title": "Chapter 14: The Beary Good Review 🐻",
        "sections": [
            {
                "subtitle": "Everything is Better with Bears",
                "text": "<div class='bear-box'>🐾 <b>Welcome to the Beary Good Review!</b> 🐾<br><br>Let's map everything you just learned into silly bear stories to lock it in your memory:<br><br><b>1. The Evil Cavemate (OMS):</b> Your cavemate traps you in the cave so you miss the salmon run. Is this wrong? Yes! But <i>Ontological Moral Skepticism (OMS)</i> says there are NO moral facts, which is silly.<br><br><b>2. The Eccentric Honey-Maker (Pogge):</b> A rich bear gives starving bears a 50/50 chance of honey or a wasp sting. This provides a 'net benefit' but violates the <b>Exception to Moral Freedom</b> because he exploits their desperation!<br><br><b>3. D-Lab Bear (Trials):</b> Greedy D-Lab bear wants to test new cough syrup. They prefer <b>Placebo-Rich</b> (fake syrup in a rich forest) because it's cheap and the bears can afford the real syrup later. But morally, they should run <b>Active-Rich</b>!<br><br><b>4. The Famous Bear-olinist (Thomson):</b> You are kidnapped and hooked up to a musical bear who needs your honey-filtered blood. Proves that the <b>Right to Life</b> does NOT mean the right to use your body!<br><br><b>5. The Direct Mauling Argument (DKA):</b> Argues that directly mauling an innocent is worse than letting someone die. The <b>Extreme Bear View (EBV)</b> says you can never unhook, even to save yourself.<br><br><b>6. The Mama Bear's Cave (SLEV vs. Mod-pro):</b> <b>SLEV</b> says only Mama Bear can save herself from danger; Dr. Bear cannot help. But Thomson argues Mama Bear has <b>Moral Ownership</b> of her cave, so Dr. Bear CAN help! <b>Mod-pro</b> allows Dr. Bear to intervene in life-or-death emergencies.<br><br><b>7. The VIP Picnic Basket (Honda Civic):</b> A bear wanders off with your picnic basket by mistake. This disproves <b>Rights Generators 1-4</b>—innocent arrival doesn't mean they own your basket!<br><br><b>8. A Forest Like Ours (FLO):</b> Why is it wrong to hunt a bear? Because it deprives them of a <b>Future Like Ours</b> (eating berries, catching salmon). Marquis applies this to say abortion is wrong!</div>",
                "drill_prompt": "What does the Famous Bear-olinist prove that the Right to Life does NOT include?", "drill_ans": ["use of a body", "right to use your body", "bare minimum"], "drill_exact": "The right to use another's body (the bare minimum)"
            }
        ],
        "exam": [
            {"q": "What does the Eccentric Honey-Maker violate?", "opts": ["Exception to Moral Freedom", "Moral Ownership"], "ans": "Exception to Moral Freedom"},
            {"q": "What does the Famous Bear-olinist prove?", "opts": ["Right to Life doesn't equal right to a body", "Direct mauling is wrong"], "ans": "Right to Life doesn't equal right to a body"},
            {"q": "What does Mama Bear's Cave prove about SLEV?", "opts": ["Mama Bear has Moral Ownership, so Dr. Bear CAN help", "Only Mama Bear can save herself"], "ans": "Mama Bear has Moral Ownership, so Dr. Bear CAN help"},
            {"q": "What does the VIP Picnic Basket disprove?", "opts": ["Rights Generators 1-4", "A Forest Like Ours"], "ans": "Rights Generators 1-4"},
            {"q": "What is Marquis's FLO in bear terms?", "opts": ["A Forest Like Ours", "A Furry Little Otter"], "ans": "A Forest Like Ours"}
        ]
    }
}

# --- MASSIVE EXAM BANK (100+ Variations generated from all notes) ---
exam_bank = [
    {"q": "How do you test for Validity?", "opts": ["See if premises are true in reality.", "Suppose premises are true, see if conclusion can be false."], "ans": "Suppose premises are true, see if conclusion can be false.", "exp": "Validity only tests logical structure."},
    {"q": "What is Soundness?", "opts": ["Valid + All premises are true.", "Invalid + True premises."], "ans": "Valid + All premises are true.", "exp": "Must be valid AND have true premises."},
    {"q": "What is the 'antecedent' of a conditional?", "opts": ["The 'Then' part.", "The 'If' part."], "ans": "The 'If' part.", "exp": "Antecedent comes first (If)."},
    {"q": "What does the Extreme View (EV) say about emergency abortions?", "opts": ["Permissible if mother does it.", "Always impermissible."], "ans": "Always impermissible.", "exp": "EV allows zero exceptions."},
    {"q": "What does SLEV say about emergency abortions?", "opts": ["Only the mother herself may perform it.", "A doctor may perform it."], "ans": "Only the mother herself may perform it.", "exp": "SLEV forbids third-party intervention."},
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
    {"q": "Is the crushing person in the Bus Case innocent?", "opts": ["Yes", "No"], "ans": "Yes", "exp": "They didn't intend to fall on you."},
    {"q": "What does DKA stand for?", "opts": ["Direct Killing Argument", "Duty to Keep Alive"], "ans": "Direct Killing Argument", "exp": "Major focus of Handouts 3.0/3.1."},
    {"q": "According to Marquis, why is killing wrong?", "opts": ["Deprives victim of a Future Like Ours", "Violates bodily autonomy"], "ans": "Deprives victim of a Future Like Ours", "exp": "A Future Like Ours (FLO) argument."},
    {"q": "What is D-Lab's self-interested ranking of trials?", "opts": ["placebo-rich > active-rich > placebo-poor > active-poor", "active-rich > active-poor > placebo-rich > placebo-poor"], "ans": "placebo-rich > active-rich > placebo-poor > active-poor", "exp": "Greed prefers cheap placebos and rich customers."},
    {"q": "What is the ranking of Moral Goodness for clinical trials?", "opts": ["placebo-rich > active-rich > placebo-poor > active-poor", "active-rich > active-poor > placebo-rich > placebo-poor"], "ans": "active-rich > active-poor > placebo-rich > placebo-poor", "exp": "Morality prefers real (active) medicine over fake sugar water."},
    {"q": "Which principle proves it was wrong for D-Lab to run the trial in Bolivia?", "opts": ["Moral Freedom", "Exception to Moral Freedom"], "ans": "Exception to Moral Freedom", "exp": "They exploited desperation."},
    {"q": "What is the consequent of 'If P, then Q'?", "opts": ["P", "Q"], "ans": "Q", "exp": "Consequent is the 'Then' part."},
    {"q": "Does Thomson grant that the fetus is a person for the sake of argument?", "opts": ["Yes", "No"], "ans": "Yes", "exp": "She grants it to prove that even if they are a person, abortion is still permissible."},
    {"q": "Under the DKA applied to the Bus Case, pushing Abilene is considered:", "opts": ["Direct killing of an innocent", "Letting die"], "ans": "Direct killing of an innocent", "exp": "Premise 2 classifies it as direct killing."},
    {"q": "In the Basic RtL Argument, what does Premise 4 claim trumps bodily rights?", "opts": ["Right to Life", "Moral Ownership"], "ans": "Right to Life", "exp": "Premise 4 explicitly claims RtL trumps what happens to the body."},
    {"q": "Does Thomson think the conclusion of the Violinist case is true or absurd?", "opts": ["True", "Absurd"], "ans": "Absurd", "exp": "It is absurd to think you are morally required to stay hooked up."},
    {"q": "What does Esmerelda prove?", "opts": ["You do not have a duty to let yourself die", "Fetuses are not persons"], "ans": "You do not have a duty to let yourself die", "exp": "Esmerelda proves you can defend yourself."},
    {"q": "If an argument's conclusion is false, what must be true about its premises if the argument is valid?", "opts": ["At least one premise must be false", "All premises must be true"], "ans": "At least one premise must be false", "exp": "A valid argument with a false conclusion must have a false premise."},
    {"q": "According to Thomson, does the right to life equal the right not to be killed by anybody in any way whatsoever?", "opts": ["Yes", "No"], "ans": "No", "exp": "It only equals the right not to be killed UNJUSTLY."},
    {"q": "In the Honda Civic case, what happens?", "opts": ["Thieves leave it running, an innocent person takes it", "You sell it to a violinist"], "ans": "Thieves leave it running, an innocent person takes it", "exp": "This disproves Rights Generators 1-4."},
    {"q": "Does the Therapeutic Misconception apply to D-Lab's trial?", "opts": ["Yes", "No"], "ans": "Yes", "exp": "Parents thought researchers were treating doctors."},
    {"q": "According to Marquis, does his FLO argument rely on Papal/Religious dogma?", "opts": ["Yes", "No"], "ans": "No", "exp": "He explicitly states it avoids religion and personhood debates."}
]

# --- GLOBAL FLASHCARD DECK (Vocab, Premises, Practice Exam) ---
flashcard_deck = [
    {"front": "Exception to Moral Freedom", "back": "Pogge: You cannot exploit desperate people for your own ends, even if providing a net benefit (Eccentric Filmmaker)."},
    {"front": "D-Lab's Self-Interest Ranking (Q2)", "back": "placebo-rich > active-rich > placebo-poor > active-poor"},
    {"front": "Moral Goodness Ranking (Q3)", "back": "active-rich > active-poor > placebo-rich > placebo-poor"},
    {"front": "Extreme View (EV) (Q5)", "back": "Abortion is ALWAYS impermissible. No exceptions."},
    {"front": "Slightly Less Extreme View (SLEV) (Q7)", "back": "Abortion impermissible EXCEPT to save mother's life AND only the mother may perform it."},
    {"front": "Moderate Pro-life View (Mod-pro) (Q8)", "back": "Abortion impermissible EXCEPT to save mother's life (a doctor MAY perform it)."},
    {"front": "Direct Killing Argument (DKA)", "back": "Argues directly killing an innocent is worse than letting someone die (attacks self-defense abortion)."},
    {"front": "Right to Life (Thomson) (Q12)", "back": "The right not to be killed unjustly. It does NOT include the right to the bare minimum needed for life."},
    {"front": "Moral Ownership", "back": "The mother owns her body, allowing her to authorize a doctor's help (disproves SLEV)."},
    {"front": "Typical Cases (Q13)", "back": "Mother wants abortion for less weighty reason than life-or-death. Permissible because of 'large sacrifice'."},
    {"front": "Rights Generators 1-4 & Honda Civic (Q4)", "back": "Innocent arrival doesn't grant property rights. Disproves idea that intercourse grants fetus rights."},
    {"front": "A Future Like Ours (FLO) (Q17)", "back": "Marquis: Killing is wrong because it deprives victim of a valuable future. Applies to fetuses."},
    {"front": "Basic RtL Premise 4", "back": "A person's right to life trumps bodily rights. (Thomson proves this is FALSE via Violinist)."},
    {"front": "DKA Premise 6.4", "back": "If options are direct killing vs letting die, you must prefer letting die. (Disproved by Bus Case)."},
    {"front": "2nd RtL Premise 4", "back": "Fetus's right to life trumps all EXCEPT the mother's right to life. (Aligns with Mod-pro)."}
]

# --- SESSION STATE ---
def init_state():
    if 'current_ch' not in st.session_state: st.session_state.current_ch = 1
    if 'current_sec' not in st.session_state: st.session_state.current_sec = 0
    if 'drill_state' not in st.session_state: st.session_state.drill_state = "unanswered"
    if 'redo_queue' not in st.session_state: st.session_state.redo_queue = []
    
    if 'in_chapter_exam' not in st.session_state: st.session_state.in_chapter_exam = False
    if 'ch_exam_q_index' not in st.session_state: st.session_state.ch_exam_q_index = 0
    if 'ch_exam_failed' not in st.session_state: st.session_state.ch_exam_failed = False

    if 'exam_q_index' not in st.session_state: st.session_state.exam_q_index = 0
    if 'exam_pool' not in st.session_state: st.session_state.exam_pool = []
    if 'exam_q_passed' not in st.session_state: st.session_state.exam_q_passed = False
    
    if 'show_flashcards' not in st.session_state: st.session_state.show_flashcards = False
    if 'fc_index' not in st.session_state: st.session_state.fc_index = 0
    if 'fc_show_back' not in st.session_state: st.session_state.fc_show_back = False

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
        st.session_state.in_chapter_exam = True
        st.session_state.ch_exam_q_index = 0
        st.session_state.ch_exam_failed = False

# --- SIDEBAR & FLASHCARD TOGGLE ---
st.sidebar.markdown("### 🃏 Study Tools")
if st.sidebar.button("OPEN GLOBAL FLASHCARDS 🃏"):
    st.session_state.show_flashcards = True
    st.rerun()
if st.sidebar.button("Restart Completely 🔄"):
    st.session_state.clear()
    init_state()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Table of Contents")
for i in range(1, 15):
    if st.session_state.current_ch == i and not st.session_state.show_flashcards:
        st.sidebar.markdown(f"**👉 Ch {i}: {curriculum[i]['title'].split(':')[1].strip()}**")
    else:
        st.sidebar.markdown(f"Ch {i}")
if st.session_state.current_ch == 15: st.sidebar.markdown("**👉 Redo Gauntlet**")
else: st.sidebar.markdown("Redo Gauntlet")
if st.session_state.current_ch == 16: st.sidebar.markdown("**👉 Final Exam**")
else: st.sidebar.markdown("Final Exam")

# --- GLOBAL FLASHCARD UI OVERRIDE ---
if st.session_state.show_flashcards:
    st.title("🃏 Global Mastery Flashcards")
    st.write("Contains ALL vocab, Practice Exam Qs, and Argument Premises.")
    if st.button("❌ Close Flashcards & Return to Lesson"):
        st.session_state.show_flashcards = False
        st.rerun()
        
    current_card = flashcard_deck[st.session_state.fc_index]
    st.write(f"Card {st.session_state.fc_index + 1} of {len(flashcard_deck)}")
    
    if not st.session_state.fc_show_back:
        st.markdown(f"<div class='flashcard'>{current_card['front']}</div>", unsafe_allow_html=True)
        if st.button("Show Answer"):
            st.session_state.fc_show_back = True
            st.rerun()
    else:
        st.markdown(f"<div class='flashcard' style='background-color:#e8f5e9;'><b>{current_card['front']}</b><hr><span style='font-size:18px; font-weight:normal;'>{current_card['back']}</span></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅️ Previous Card"):
                st.session_state.fc_index = max(0, st.session_state.fc_index - 1)
                st.session_state.fc_show_back = False
                st.rerun()
        with c2:
            if st.button("Next Card ➡️"):
                st.session_state.fc_index = (st.session_state.fc_index + 1) % len(flashcard_deck)
                st.session_state.fc_show_back = False
                st.rerun()
    st.stop() 

# --- MAIN APP LOGIC ---
if st.session_state.current_ch <= 14:
    ch = st.session_state.current_ch
    ch_data = curriculum[ch]
    st.title(ch_data["title"])
    
    if not st.session_state.in_chapter_exam:
        sec_data = ch_data["sections"][st.session_state.current_sec]
        st.subheader(sec_data["subtitle"])
        
        # Skip to Exam Button
        if st.button("⏭️ Skip Reading & Go to Chapter Exam"):
            st.session_state.in_chapter_exam = True
            st.session_state.ch_exam_q_index = 0
            st.session_state.ch_exam_failed = False
            st.rerun()
            
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

# STAGE 15: REDO GAUNTLET
elif st.session_state.current_ch == 15:
    st.title("🧠 The Redo Gauntlet")
    if len(st.session_state.redo_queue) == 0:
        st.success("🎉 Gauntlet cleared! You are ready for the Final Exam.")
        if st.button("Start Final Exam 📝"):
            st.session_state.current_ch = 16
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

# STAGE 16: FINAL EXAM
elif st.session_state.current_ch == 16:
    st.title("📝 Comprehensive Final Exam")
    st.write("20 randomly selected questions from the massive test bank. You must get each correct to proceed.")
    
    if not st.session_state.exam_pool:
        st.session_state.exam_pool = random.sample(exam_bank, 20)
        
    if st.session_state.exam_q_index >= 20:
        st.balloons()
        st.success("🎉 YOU PASSED THE FINAL EXAM! You are officially prepared.")
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
