import streamlit as st

# --- PAGE CONFIGURATION & BEAR THEME ---
st.set_page_config(page_title="Beary Good Phil 4 Adventure", page_icon="🐻", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #f4f1ea;
        color: #3e2723;
    }
    h1, h2, h3 {
        color: #5d4037;
        font-family: 'Courier New', Courier, monospace;
    }
    .story-box {
        background-color: #e7cda2;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #8d6e63;
        margin-bottom: 20px;
        font-size: 18px;
    }
    .vocab-box {
        background-color: #c8e6c9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .drill-box {
        background-color: #bbdefb;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1976d2;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #795548;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #5d4037;
        color: #ffb300;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'learned_vocab' not in st.session_state:
    st.session_state.learned_vocab = []
if 'sub_stage' not in st.session_state:
    st.session_state.sub_stage = 0

def next_stage():
    st.session_state.stage += 1
    st.session_state.sub_stage = 0

def add_vocab(word):
    if word not in st.session_state.learned_vocab:
        st.session_state.learned_vocab.append(word)

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.stage = 0
    st.session_state.learned_vocab = []
    st.session_state.sub_stage = 0

# --- SIDEBAR: VOCAB TRACKER ---
st.sidebar.title("🐾 Bear Tracker: Vocab")
st.sidebar.markdown("Watch your knowledge grow!")
st.sidebar.markdown("---")

if st.session_state.learned_vocab:
    for word in st.session_state.learned_vocab:
        st.sidebar.markdown(f"✅ **{word}**")
else:
    st.sidebar.write("*No words learned yet. Start exploring!*")

# --- THE INTERACTIVE LESSON ---

if st.session_state.stage == 0:
    st.title("🐻 Beary Good Phil 4 Adventure 🐾")
    st.markdown("### An Interactive Ethics Story")
    st.markdown("Welcome to your study adventure! Let's travel through **Moral Skepticism**, **Clinical Trials**, and **The Ethics of Abortion**.")
    st.markdown("⚠️ **NEW RULE:** Professor Bear is going to make you *type* the answers to drill them into your brain. Spelling counts (mostly)!")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Start the Adventure! 🐾"):
            next_stage()
            st.rerun()

# ---------------------------------------------------------
# CHAPTER 1: MORAL SKEPTICISM 
# ---------------------------------------------------------
elif st.session_state.stage == 1:
    st.title("Chapter 1: The Evil Roommate")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    Your roommate locks you in the bathroom from the outside for hours so they can study and beat the curve!
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.sub_stage == 0:
        st.write("Was it wrong for your roommate to lock you in the bathroom?")
        if st.button("Yes, absolutely wrong!"):
            st.session_state.sub_stage = 1
            st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> Yes! But we must separate the little weights on the scale from the final verdict.<br><br>
        1. <b>Moral Considerations</b>: The reasons for/against an action.<br>
        2. <b>All-Things-Considered Moral Norms</b>: The final verdict (e.g., "morally impermissible").
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='drill-box'><b>✏️ Drill Time:</b> What do we call the final, absolute moral verdict of an action? (Hint: Type 'all-things-considered')</div>", unsafe_allow_html=True)
        ans = st.text_input("Type your answer here:")
        
        if ans.lower().strip() == "all-things-considered" or ans.lower().strip() == "all things considered":
            st.success("Correct! You locked it in.")
            add_vocab("Moral Considerations")
            add_vocab("All-Things-Considered Moral Norms")
            if st.button("Next Chapter ✈️"):
                next_stage()
                st.rerun()
        elif ans:
            st.error("Not quite. Check the spelling in the hint!")

# ---------------------------------------------------------
# CHAPTER 2: CLINICAL TRIALS & POGGE
# ---------------------------------------------------------
elif st.session_state.stage == 2:
    st.title("Chapter 2: The Surfaxin Trial")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You are the CEO of D-Lab testing Surfaxin in Bolivia. Half the babies get the drug, half get a placebo, even though good treatments exist in the US!
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.sub_stage == 0:
        st.write("Parents are confused. They think you are trying to heal their babies, not just run an experiment.")
        if st.button("Learn the Vocab Word for this!"):
            st.session_state.sub_stage = 1
            st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> <br><br>
        <b>The Therapeutic Misconception:</b> When a patient confuses a <i>researcher's</i> main goal (getting data) with a <i>doctor's</i> main goal (patient health).<br><br>
        Pogge also notes that even if you provide a benefit, you can't exploit desperation. This breaks the <b>Exception to Moral Freedom</b>.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='drill-box'><b>✏️ Drill Time:</b> What is it called when a subject confuses a researcher for a treating doctor?</div>", unsafe_allow_html=True)
        ans1 = st.text_input("Type your answer here:")
        
        if "therapeutic misconception" in ans1.lower().strip():
            st.success("Nailed it! Let's do one more.")
            st.markdown("<div class='drill-box'><b>✏️ Drill Time 2:</b> Pogge says taking advantage of desperate people violates the Exception to Moral _________.</div>", unsafe_allow_html=True)
            ans2 = st.text_input("Fill in the blank:")
            
            if ans2.lower().strip() == "freedom":
                add_vocab("Therapeutic Misconception")
                add_vocab("Exception to Moral Freedom")
                if st.button("Next Chapter 🏥"):
                    next_stage()
                    st.rerun()
            elif ans2:
                st.error("Hint: It rhymes with 'boredom'!")
        elif ans1:
            st.error("Hint: Starts with 'Therapeutic...'")

# ---------------------------------------------------------
# CHAPTER 3: THOMSON & THE VIOLINIST 
# ---------------------------------------------------------
elif st.session_state.stage == 3:
    st.title("Chapter 3: The Famous Violinist")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You are kidnapped and hooked up to a famous violinist to filter his blood for 9 months.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.sub_stage == 0:
        if st.button("Does his 'Right to Life' mean he gets to use your body?"):
            st.session_state.sub_stage = 1
            st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> NO!<br><br>
        Thomson argues that the <b>Right to Life</b> does NOT include the right to be given the bare minimum one needs for continued life (like the use of someone's body).<br>
        This directly attacks the <b>Extreme View (EV)</b>, which says abortion is always impermissible.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='drill-box'><b>✏️ Drill Time:</b> What specific view claims abortion is ALWAYS impermissible, even to save the mother? (Type the 2-word phrase)</div>", unsafe_allow_html=True)
        ans = st.text_input("Type your answer here:")
        
        if ans.lower().strip() == "extreme view" or ans.lower().strip() == "the extreme view":
            st.success("Excellent.")
            add_vocab("Right to Life (Thomson's definition)")
            add_vocab("Extreme View (EV)")
            if st.button("Next Chapter 🚗"):
                next_stage()
                st.rerun()
        elif ans:
            st.error("Hint: Extreme...")

# ---------------------------------------------------------
# CHAPTER 4: THE HONDA CIVIC CASE
# ---------------------------------------------------------
elif st.session_state.stage == 4:
    st.title("Chapter 4: The VIP Honda Civic")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    Thieves leave your VIP Honda Civic running. An innocent guy thinks it's his car and drives it home.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.sub_stage == 0:
        if st.button("Does he have a right to your car now?"):
            st.session_state.sub_stage = 1
            st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> Nope, it's still your car.<br><br>
        Professor McHose uses this specific case as a <b>Counterexample</b> to Rights Generators #1, #2, and #3. An innocent arrival doesn't automatically grant a moral right to use your property (or body).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='drill-box'><b>✏️ Drill Time:</b> In logic, when you provide a scenario that disproves a rule (like the Honda Civic case disproving the rights generators), what is that scenario called?</div>", unsafe_allow_html=True)
        ans = st.text_input("Type your answer here:")
        
        if "counterexample" in ans.lower().strip() or "counter example" in ans.lower().strip():
            st.success("You got it!")
            add_vocab("Rights Generators 1-3")
            add_vocab("Counterexample")
            if st.button("Next Chapter 🔮"):
                next_stage()
                st.rerun()
        elif ans:
            st.error("Hint: Counter-something...")

# ---------------------------------------------------------
# CHAPTER 5: MARQUIS
# ---------------------------------------------------------
elif st.session_state.stage == 5:
    st.title("Chapter 5: Marquis")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    Don Marquis asks you: <i>"Why is it wrong to kill you, an adult human being, right now?"</i>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.sub_stage == 0:
        if st.button("Learn Marquis's Answer!"):
            st.session_state.sub_stage = 1
            st.rerun()

    elif st.session_state.sub_stage == 1:
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> <br><br>
        <b>A Future Like Ours (FLO):</b> Marquis argues that killing is wrong because it deprives the victim of a valuable future. He extends this to fetuses, saying they also possess a "future like ours."
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='drill-box'><b>✏️ Drill Time:</b> What is the exact 4-word phrase (or 3-letter acronym) Marquis uses to describe what is lost when someone is killed?</div>", unsafe_allow_html=True)
        ans = st.text_input("Type your answer here:")
        
        if ans.lower().strip() in ["a future like ours", "future like ours", "flo"]:
            st.success("Perfect!")
            add_vocab("A Future Like Ours (FLO)")
            if st.button("Finish Adventure! 🎉"):
                next_stage()
                st.rerun()
        elif ans:
            st.error("Hint: A F_____ L___ O___ (or FLO)")

# ---------------------------------------------------------
# END SCREEN
# ---------------------------------------------------------
elif st.session_state.stage == 6:
    st.balloons()
    st.title("🎉 You Did It! 🎉")
    st.markdown("Look at that full sidebar of vocabulary! You are officially ready for Exam 2.")
    
    if st.button("Play Again?"):
        reset_game()
        st.rerun()
