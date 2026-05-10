import streamlit as st

# --- PAGE CONFIGURATION & BEAR THEME ---
st.set_page_config(page_title="Beary Good Phil 4 Adventure", page_icon="🐻", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #f4f1ea;
        color: #3e2723;
    }
    h1, h2, h3 {
        color: #5d4037;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
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
# We use this to keep track of what "page" or "chapter" of the story you are on.
if 'stage' not in st.session_state:
    st.session_state.stage = 0

def next_stage():
    st.session_state.stage += 1

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.stage = 0

# --- THE INTERACTIVE LESSON ---

if st.session_state.stage == 0:
    st.title("🐻 Beary Good Phil 4 Adventure 🐾")
    st.markdown("### An Interactive Ethics Story")
    st.markdown("Welcome to your study adventure! Instead of just answering questions, you are going to *live* through the thought experiments from Professor McHose's class.")
    st.markdown("We will travel through **Moral Skepticism**, **Clinical Trials**, and **The Ethics of Abortion**. Let's learn the fancy vocab using simple stories!")
    
    if st.button("Start the Adventure! 🐾"):
        next_stage()
        st.rerun()

# ---------------------------------------------------------
# CHAPTER 1: MORAL SKEPTICISM (Handouts 1.0 & 1.1)
# ---------------------------------------------------------
elif st.session_state.stage == 1:
    st.title("Chapter 1: The Evil Roommate")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You have a massive philosophy exam tomorrow. You leave your dorm room for a second, and when you return, your roommate locks you in the bathroom from the outside! 
    They yell through the door: <i>"I'm keeping you in here so I can study and beat the curve!"</i> They leave you locked in for hours.
    </div>
    """, unsafe_allow_html=True)

    st.write("Was it wrong for your roommate to lock you in the bathroom?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, absolutely wrong!"):
            st.session_state.ch1_answered = True
    with col2:
        if st.button("Maybe not?"):
            st.session_state.ch1_answered = True

    if st.session_state.get('ch1_answered', False):
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> Almost 100% of people say YES, it was wrong. But philosophers use this to separate two important vocab words:<br><br>
        1. <b>Moral Considerations (or Moral Reasons):</b> The little weights on the scale. (e.g., "It made you sad," "It helped them pass.")<br>
        2. <b>All-Things-Considered Moral Norms (or Conclusive Moral Norms):</b> The final verdict after weighing everything. This is when we say something is officially "Morally Impermissible" (wrong).
        <br><br>
        If you think there are NO moral facts at all, you might be an <b>Ontological Moral Skeptic (OMS)</b>. But getting locked in a bathroom makes OMS feel pretty silly, right?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Next Chapter: Off to Bolivia ✈️", on_click=next_stage):
            pass

# ---------------------------------------------------------
# CHAPTER 2: CLINICAL TRIALS & POGGE (Handouts 2.0 - 2.2)
# ---------------------------------------------------------
elif st.session_state.stage == 2:
    st.title("Chapter 2: The Surfaxin Trial")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You are now the CEO of "D-Lab", a pharmaceutical company. You have a new drug called Surfaxin that helps premature babies breathe. You want to test it. 
    You go to Bolivia because it's cheaper. You run a trial where half the dying babies get Surfaxin, and half get a <b>placebo</b> (fake treatment like sugar water)—even though good treatments already exist in the US!
    </div>
    """, unsafe_allow_html=True)

    st.write("Why might the parents of the Bolivian babies be confused about your intentions?")
    
    if st.button("They think you are trying to heal their babies, not just run an experiment."):
        st.session_state.ch2_answered = True
    if st.button("They think you are giving them money."):
        st.session_state.ch2_answered = True

    if st.session_state.get('ch2_answered', False):
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> You nailed it! This confusion has a specific name you need for the test:<br><br>
        <b>The Therapeutic Misconception:</b> This is when a patient confuses a <i>researcher's</i> main goal (getting info/data) with a <i>doctor's</i> main goal (preserving patient health).<br><br>
        Philosopher Thomas Pogge compares this to an <b>Eccentric Filmmaker</b> who gives poor people boxes that either have $30,000 or a paint-bomb inside just for a laugh. Pogge argues that even if you are providing a "net benefit" to some, you can't just take advantage of desperate people (This is called the <b>Exception to Moral Freedom</b>).
        </div>
        """, unsafe_allow_html=True)
        if st.button("Next Chapter: A Strange Hospital 🏥", on_click=next_stage):
            pass

# ---------------------------------------------------------
# CHAPTER 3: THOMSON & THE VIOLINIST (Handouts 3.0 - 3.2)
# ---------------------------------------------------------
elif st.session_state.stage == 3:
    st.title("Chapter 3: The Famous Violinist")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You wake up in a hospital bed. You look to your left and see a famously talented violinist hooked up to your kidneys with tubes! 
    The Society of Music Lovers kidnapped you because only your blood type can filter his blood. If you unplug him right now, he will die. If you stay in bed for 9 months, he will be cured.
    </div>
    """, unsafe_allow_html=True)

    st.write("Does the violinist's 'Right to Life' mean you are morally obligated to stay plugged in for 9 months?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, a right to life means a right to whatever you need to survive."):
            st.session_state.ch3_answered = True
    with col2:
        if st.button("No, his right to life doesn't give him the right to use YOUR body."):
            st.session_state.ch3_answered = True

    if st.session_state.get('ch3_answered', False):
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> According to philosopher Judith Jarvis Thomson, the answer is NO!<br><br>
        Thomson argues that the <b>Right to Life</b> does NOT include the right to be given the bare minimum one needs for continued life (like the use of someone else's body).<br><br>
        She is attacking the <b>Extreme View (EV)</b>, which claims abortion is <i>always</i> impermissible, even to save the mother's life. Thomson proves that just because a fetus has a right to life, it doesn't automatically mean it has a right to use the mother's body!
        </div>
        """, unsafe_allow_html=True)
        if st.button("Next Chapter: Dude, Where's My Car? 🚗", on_click=next_stage):
            pass

# ---------------------------------------------------------
# CHAPTER 4: THE HONDA CIVIC CASE (Handout 3.3)
# ---------------------------------------------------------
elif st.session_state.stage == 4:
    st.title("Chapter 4: The VIP Honda Civic")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You paid extra for VIP parking at a concert. A gang of sophisticated car thieves breaks in, but they get spooked by the cops. They leave your Honda Civic running with the door open. 
    An innocent guy walks out of the concert, thinks your Honda is his Honda, and drives it home.
    </div>
    """, unsafe_allow_html=True)

    st.write("Does this innocent guy now have a 'Right' to your car just because he didn't do anything malicious?")
    
    if st.button("Nope, it's still my car!"):
        st.session_state.ch4_answered = True

    if st.session_state.get('ch4_answered', False):
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> Exactly. Professor McHose uses this highly specific case as a <b>counterexample</b> to Rights Generators #1, #2, and #3.<br><br>
        Just because the guy is innocent and ended up in your car by accident (or through the actions of a third party), he doesn't gain the moral right to keep your car. This analogy is used to explore how a fetus might (or might not) acquire the right to use a mother's body!
        </div>
        """, unsafe_allow_html=True)
        if st.button("Next Chapter: Marquis and the Future 🔮", on_click=next_stage):
            pass

# ---------------------------------------------------------
# CHAPTER 5: MARQUIS (Handout 4)
# ---------------------------------------------------------
elif st.session_state.stage == 5:
    st.title("Chapter 5: A Future Like Ours")
    
    st.markdown("""
    <div class='story-box'>
    <b>The Situation:</b><br>
    You meet philosopher Don Marquis. He doesn't want to talk about religion or whether a fetus is a "person." Instead, he asks you a simple question: 
    <i>"Why is it wrong to kill you, an adult human being, right now?"</i>
    </div>
    """, unsafe_allow_html=True)

    st.write("According to Marquis, what makes killing an adult so terribly wrong?")
    
    if st.button("Because it causes pain."):
        st.session_state.ch5_answered = True
    if st.button("Because it deprives the victim of all their future experiences and joys."):
        st.session_state.ch5_answered = True

    if st.session_state.get('ch5_answered', False):
        st.markdown("""
        <div class='vocab-box'>
        <b>🐻 Professor Bear says:</b> You got it! Marquis has a very famous argument:<br><br>
        <b>A Future Like Ours (FLO):</b> Marquis argues that killing is wrong because it deprives someone of a valuable future. Since a fetus has a "future like ours" waiting for it, killing a fetus is just as wrong as killing an adult.<br><br>
        This argument avoids messy debates about "personhood" and focuses strictly on the loss of future value.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Finish Adventure! 🎉", on_click=next_stage):
            pass

# ---------------------------------------------------------
# END SCREEN
# ---------------------------------------------------------
elif st.session_state.stage == 6:
    st.balloons()
    st.title("🎉 You Did It! 🎉")
    st.markdown("""
    You have successfully navigated through the major thought experiments of your exam!
    
    **Review Checklist before tomorrow:**
    * ✅ **Moral Skepticism:** Roommate case, Moral considerations vs All-things-considered norms.
    * ✅ **Clinical Trials (Pogge):** Surfaxin, Therapeutic Misconception, Eccentric Filmmaker.
    * ✅ **Abortion (Thomson):** The Violinist, Extreme View, Honda Civic case.
    * ✅ **Abortion (Marquis):** A Future Like Ours (FLO).
    
    Get some sleep, eat a good breakfast, and go crush Exam 2! 🐻🐾
    """)
    
    if st.button("Play Again?"):
        reset_game()
        st.rerun()
