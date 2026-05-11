import streamlit as st
import re
import random

# --- PAGE CONFIGURATION & THEME ---
st.set_page_config(page_title="Phil 4 Master Study App", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f1ea; color: #3e2723; }
    h1, h2, h3 { color: #5d4037; font-family: 'Courier New', Courier, monospace; }
    .cover-box { background-color: #fff8e1; padding: 50px; border-radius: 20px; border: 4px solid #ffb300; margin-bottom: 30px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .story-box { background-color: #e7cda2; padding: 20px; border-radius: 15px; border: 2px solid #8d6e63; margin-bottom: 20px; font-size: 18px; line-height: 1.6; }
    .drill-box { background-color: #bbdefb; padding: 15px; border-radius: 10px; border-left: 5px solid #1976d2; margin-bottom: 15px; }
    .exam-box { background-color: #e1bee7; padding: 20px; border-radius: 10px; border: 3px solid #8e24aa; margin-bottom: 15px; }
    .flashcard { background-color: #ffffff; padding: 40px; border-radius: 15px; border: 3px dashed #8d6e63; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #795548; color: white; border-radius: 10px; width: 100%; font-weight: bold; padding: 15px; font-size: 18px; }
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
                "subtitle": "Handout 2.2 p10-17",
                "text": "In Handout 2.2, Thomas Pogge examines the ethics of pharmaceutical testing in developing nations. He introduces the **Exception to Moral Freedom**: You cannot exploit desperate people for your own ends, even if you provide a 'net benefit'. He illustrates this with the 'Eccentric Filmmaker' case, where a wealthy individual gives starving people a 50/50 chance at $30,000 or a paint bomb for his own amusement. Though the money provides an overall net benefit to the community, taking advantage of their extreme poverty remains morally grotesque.\n\nWhen evaluating clinical trials, we must distinguish between a company's self-interest and actual moral goodness. A greedy company like D-Lab ranks trial types based on cost and market logic: **Placebo-rich > Active-rich > Placebo-poor > Active-poor**. They prefer placebos because they are much cheaper and faster to run, and they prefer rich countries because citizens can actually afford the drug once it is approved. However, true moral goodness prioritizes real medicine over fake sugar-water, ranking them: **Active-rich > Active-poor > Placebo-rich > Placebo-poor**.\n\nBecause the US FDA bans placebo trials when existing cures are already available (like for Respiratory Distress Syndrome in premature babies), D-Lab cannot legally run a Placebo-rich trial. Instead, they choose to run a Placebo-poor trial in Bolivia. Because they do this simply because it is cheaper and the foreign laws are looser, Pogge argues they violate the Exception to Moral Freedom by exploiting the desperation of the Bolivian parents. These parents also suffer from the **Therapeutic Misconception**, confusing the researcher's primary goal (gathering data) with a doctor's primary goal (preserving patient health).",
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
                "text": "The Basic Right to Life Argument begins by assuming the fetus is a person with a right to life, and concludes abortion is impermissible. Thomson famously grants this assumption (that the fetus is a person) for the sake of argument. However, she attacks the logic using the **Basic Violinist Case**. Imagine you are kidnapped and your kidneys are hooked up to a famous violinist to filter his blood. The violinist is a person with a right to life, but that does NOT mean he has a right to use your kidneys. Thus, the primary purpose of the Violinist case is to show a right to life does not guarantee use of another person's body.\n\nThomson then strictly categorizes pro-life views. The **Extreme View (EV)** takes an absolute stance: abortion is ALWAYS impermissible. It allows absolutely no exceptions, not even to save the mother's life.\n\nThe **Direct Killing Argument (DKA)** is often used to support EV by arguing that directly killing an innocent person is morally worse than passively letting someone die (the mother). Thomson defines 'direct killing' strictly as killing as an end in itself, or as a means to some end.",
                "drill_prompt": "What is the ONE WORD name of the view that abortion is ALWAYS impermissible? (Hint: _______ View)", "drill_ans": ["extreme"], "drill_exact": "Extreme"
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
                "text": "Thomson provides counterexamples to attack Premise 6.4 of the DKA (which claims you must always prefer letting yourself die rather than directly killing an innocent). She uses the **Chet & Abilene (Bus) Case**: If Abilene is thrown in a bus crash and is going to crush Chet to death, Chet is morally permitted to push her off to save his life. Abilene is considered perfectly *innocent* because she didn't intend to fall, but Chet can still directly kill her to survive. Similarly, the **Esmerelda** case shows that a person does not have a strict moral duty to simply let themselves die.\n\nNext, Thomson examines the **Slightly Less Extreme View (SLEV)**. SLEV claims abortion is impermissible EXCEPT to save the mother's life, BUT with a strict condition: only the mother herself can perform it. A doctor or third-party is strictly forbidden from intervening.\n\nThomson attacks SLEV using **Moral Ownership**. Because the mother morally owns her body as her property, she has the right to authorize a third party (the doctor) to help her defend it.",
                "drill_prompt": "Under SLEV, can a doctor perform a life-saving abortion? (Yes/No)", "drill_ans": ["no"], "drill_exact": "No"
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
                "text": "The **Moderate Pro-life View (Mod-pro)** claims abortion is impermissible EXCEPT to save the mother's life. Unlike SLEV, Mod-pro explicitly allows a doctor to perform the procedure. \n\nThis aligns with the 2nd version of the RtL Argument. Premise 4 of this argument states: A fetus' right to life trumps all considerations *with the possible exception of the mother's right to life*.\n\nThomson attacks the core of these arguments by analyzing moral rights. Thomson defines the **Right to Life** simply as the right not to be killed unjustly. Crucially, it does NOT include the right to be given the bare minimum one needs for continued life. Therefore, even if a fetus has a Right to Life, that right alone does not guarantee them the right to use the mother's body for nine months.",
                "drill_prompt": "What is the ONE WORD name of the view that allows a doctor to perform a life-saving abortion? (Hint: _______ Pro-life View)", "drill_ans": ["moderate"], "drill_exact": "Moderate"
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
                "text": "**Typical Cases** are those where the mother wants an abortion for less weighty reasons than preserving her own life (i.e., it is not a medical emergency, she simply does not wish to be a parent). Thomson argues abortion is still permissible here because the mother would have to make a 'large sacrifice' to carry the fetus, and the fetus has no inherent right to demand that sacrifice.\n\nPro-lifers often counter this by using **Rights Generators 1-4**, arguing that because the mother engaged in intercourse (sometimes recklessly), she voluntarily generated a right for the fetus to use her body. Thomson disproves ALL of these rights generators with the **Identical Cars (VIP Honda Civic)** case. If you pay for VIP parking, but thieves break in and leave your car running, and an innocent person accidentally drives it away thinking it's theirs, they do not gain a moral right to keep your car. This proves that an innocent arrival—even one stemming from your own actions or third-party interference—doesn't automatically grant property or bodily rights.",
                "drill_prompt": "What type of case involves a less weighty reason than saving the mother's life? (One word)", "drill_ans": ["typical"], "drill_exact": "Typical"
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
                "text": "Professor McHose tests heavily on logical structure.\n\nTo test an argument for **Validity**: You must suppose that all the premises are true. If it is mathematically/logically possible for the conclusion to be false while the premises are true, the argument is INVALID. Validity only cares about the structure of the argument, not the real world.\n\n**Soundness** is a higher bar. An argument is Sound ONLY if it is Valid AND all of its premises are actually true in reality. Therefore, if an argument is perfectly valid, but one of the premises is factually false in the real world, the argument is NOT sound.\n\nWe also use **Conditionals**, which are 'If/Then' statements. The **Antecedent** is the 'If' part of the sentence (the condition). The **Consequent** is the 'Then' part (the result).",
                "drill_prompt": "If an argument is valid AND all its premises are actually true, the argument is ______.", "drill_ans": ["sound"], "drill_exact": "Sound"
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
                "text": "This is the classic argument:\n1. By the Nth week of pregnancy, the fetus is a person. \n2. Every person has a right to life. \n3. So, by the Nth week, the fetus has a right to life. \n4. A person's right to life (a) trumps any rights another person might have regarding what happens in and/or to their body and (b) makes it impermissible to kill the person.\n5. Having an abortion would kill the fetus. \nC: It is morally impermissible to have an abortion in or after the Nth week of pregnancy.\n\nPremise 4 is the crucial step Thomson attacks.",
                "drill_prompt": "Which premise number claims the right to life trumps bodily rights? (Type the number)", "drill_ans": ["4", "four"], "drill_exact": "4"
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
                "text": "When applied to the Violinist, the logic dictates: \n1. Violinist is a person.\n2. Persons have a Right to Life (RtL).\n3. Violinist has RtL.\n4. RtL trumps bodily rights.\n5. Unhooking kills violinist.\nC: It is impermissible to unhook yourself.\n\nThomson points out that the conclusion is absurd/false—you are kidnapped and hooked up to tubes, you absolutely CAN unhook yourself! Because the logic is valid but the conclusion is false, it proves that Premise 4 (that RtL trumps bodily rights) must be false.",
                "drill_prompt": "Because the conclusion of the Violinist case is false, we know the argument is not _______.", "drill_ans": ["sound"], "drill_exact": "Sound"
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
                "text": "The DKA isolates passive versus active actions.\nPremise 2: Abortion is direct killing. \nPremise 5: Not aborting is merely letting the mother die. \nPremise 6.4: If your only options are directly killing an innocent or letting a person die, you MUST prefer letting the person die. \nC: Impermissible to abort.\n\nThomson will target 6.4 and an alternative version of it, 6.2 (which claims direct killing is murder).",
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
                "text": "Applying DKA to the Violinist uses Premise 6.2: Direct killing an innocent is murder, which is always and absolutely impermissible. \nC: Impermissible to unhook, even to save your life.\n\nCalling the act of unhooking 'murder' makes the argument valid, but clearly unsound. Thomson shows this is absurd, proving that unhooking yourself to save your own life is NOT murder.",
                "drill_prompt": "Does Thomson believe you must stay hooked up to save your life? (Yes/No)", "drill_ans": ["no"], "drill_exact": "No"
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
                "text": "The DKA says Chet cannot push the crushing passenger (Abilene) off of him, because pushing her is direct killing, and letting her crush him is just letting himself die.\n\nThomson shows this is completely false. Chet CAN push an innocent threat off to save his own life. The DKA's reliance on 'letting die' over 'direct killing' falls apart in self-defense scenarios.",
                "drill_prompt": "Who is crushing Chet in the Bus Case? (One word name)", "drill_ans": ["abilene"], "drill_exact": "Abilene"
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
                "text": "Premise 4: A fetus' right to life trumps all considerations, with the possible exception of the mother's right to life. \nC: If a woman does not need an abortion to save her life (a Typical Case), it is impermissible.\n\nThis argument aligns with the Mod-pro view. However, Thomson rejects it because even in non-emergencies, forcing someone to act as an incubator might be an unjustifiably 'large sacrifice' that the fetus has no right to demand.",
                "drill_prompt": "In the 2nd RtL Argument, Premise 4 makes a possible exception for the mother's _____. (One word)", "drill_ans": ["life"], "drill_exact": "Life"
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
                "text": "Don Marquis intentionally avoids getting bogged down in religious dogma, the 'personhood' debate, or speciesism. Instead, he focuses entirely on the loss of life's experiences. He asks: Why is killing an adult human being wrong? Because it deprives them of a valuable future—all their projects, enjoyments, and experiences. He calls this concept **A Future Like Ours (FLO)**.\n\nBecause a fetus also possesses a future like ours waiting for it, killing a fetus deprives it of that exact same value. Therefore, abortion is in the exact same moral category as killing an adult human being. This also cleanly explains why killing infants is wrong, even though they aren't fully rational 'persons' yet.",
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
    {"front": "D-Lab's Self-Interest Ranking", "back": "placebo-rich > active-rich > placebo-poor > active-poor"},
    {"front": "Moral Goodness Ranking", "back": "active-rich > active-poor > placebo-rich > placebo-poor"},
    {"front": "Extreme View (EV)", "back": "Abortion is ALWAYS impermissible. No exceptions."},
    {"front": "Slightly Less Extreme View (SLEV)", "back": "Abortion impermissible EXCEPT to save mother's life AND only the mother may perform it."},
    {"front": "Moderate Pro-life View (Mod-pro)", "back": "Abortion impermissible EXCEPT to save mother's life (a doctor MAY perform it)."},
    {"front": "Direct Killing Argument (DKA)", "back": "Argues directly killing an innocent is worse than letting someone die (attacks self-defense abortion)."},
    {"front": "Right to Life (Thomson)", "back": "The right not to be killed unjustly. It does NOT include the right to the bare minimum needed for life."},
    {"front": "Moral Ownership", "back": "The mother owns her body, allowing her to authorize a doctor's help (disproves SLEV)."},
    {"front": "Typical Cases", "back": "Mother wants abortion for less weighty reason than life-or-death. Permissible because of 'large sacrifice'."},
    {"front": "Rights Generators 1-4 & Honda Civic", "back": "Innocent arrival doesn't grant property rights. Disproves idea that intercourse grants fetus rights."},
    {"front": "A Future Like Ours (FLO)", "back": "Marquis: Killing is wrong because it deprives victim of a valuable future. Applies to fetuses."},
    {"front": "Basic RtL Premise 4", "back": "A person's right to life trumps bodily rights. (Thomson proves this is FALSE via Violinist)."},
    {"front": "DKA Premise 6.4", "back": "If options are direct killing vs letting die, you must prefer letting die. (Disproved by Bus Case)."},
    {"front": "2nd RtL Premise 4", "back": "Fetus's right to life trumps all EXCEPT the mother's right to life. (Aligns with Mod-pro)."}
]

# --- SESSION STATE ---
def init_state():
    if 'current_ch' not in st.session_state: st.session_state.current_ch = 0
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
if st.session_state.current_ch == 0 and not st.session_state.show_flashcards:
    st.sidebar.markdown("**👉 🏠 Cover Page**")
else:
    st.sidebar.markdown("🏠 Cover Page")

for i in range(1, 14):
    if st.session_state.current_ch == i and not st.session_state.show_flashcards:
        st.sidebar.markdown(f"**👉 Ch {i}: {curriculum[i]['title'].split(':')[1].strip()}**")
    else:
        st.sidebar.markdown(f"Ch {i}")

if st.session_state.current_ch == 14: st.sidebar.markdown("**👉 Redo Gauntlet**")
else: st.sidebar.markdown("Redo Gauntlet")
if st.session_state.current_ch == 15: st.sidebar.markdown("**👉 Final Exam**")
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

# --- COVER PAGE (Ch 0) ---
if st.session_state.current_ch == 0:
    st.title("📚 Philosophy 4 Master Class")
    st.markdown("### Your Ultimate Interactive Study Guide for Exam 2")
    st.markdown("""
        <div class='cover-box'>
            <h2>Welcome!</h2>
            <p>This app contains the <b>ENTIRE</b> course material for Exam 2, structured exactly to Professor McHose's specifications.</p>
            <p>You will explore:</p>
            <ul style='text-align: left; display: inline-block;'>
                <li><b>Thomas Pogge:</b> Clinical Trials & The Exception to Moral Freedom</li>
                <li><b>Judith Jarvis Thomson:</b> The Ethics of Abortion, Rights, & Counterexamples</li>
                <li><b>Don Marquis:</b> A Future Like Ours (FLO)</li>
                <li><b>Logic:</b> Validity, Soundness, and Conditionals</li>
            </ul>
            <br><br>
            <p><i>Master each chapter, clear the Redo Gauntlet, and conquer the 20-Question Final Exam!</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 START THE LESSON", use_container_width=True):
        st.session_state.current_ch = 1
        st.rerun()

# --- MAIN APP LOGIC (Ch 1-13) ---
elif st.session_state.current_ch <= 13:
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

# STAGE 14: REDO GAUNTLET
elif st.session_state.current_ch == 14:
    st.title("🧠 The Redo Gauntlet")
    if len(st.session_state.redo_queue) == 0:
        st.success("🎉 Gauntlet cleared! You are ready for the Final Exam.")
        if st.button("Start Final Exam 📝"):
            st.session_state.current_ch = 15
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

# STAGE 15: FINAL EXAM
elif st.session_state.current_ch == 15:
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
