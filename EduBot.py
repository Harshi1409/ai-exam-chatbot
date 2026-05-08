from groq import Groq
import streamlit as st
import json
import time

# ── API CLIENT ──────────────────────────────────────────────────────
client = Groq(api_key="paste-your-groq-key-here")

# ── PAGE CONFIG ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduBot AI — Smart Exam Prep",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg: #060612;
    --surface: #0d0d1f;
    --card: #12122a;
    --card2: #16163a;
    --border: #1e1e4a;
    --accent: #6366f1;
    --accent2: #8b5cf6;
    --cyan: #22d3ee;
    --green: #10b981;
    --yellow: #f59e0b;
    --pink: #ec4899;
    --red: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
}

* { font-family: 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(34,211,238,0.05) 0%, transparent 50%) !important;
}

.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div { background: var(--card) !important; }

.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    transition: all 0.3s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
}

.stSlider > div > div > div { background: var(--accent) !important; }
.stRadio label, .stCheckbox label { color: var(--text) !important; font-size: 14px !important; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--card) !important;
    border-radius: 14px !important;
    padding: 0.4rem !important;
    gap: 0.2rem !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.4) !important;
}

.streamlit-expanderHeader {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-weight: 600 !important;
}

.stProgress > div > div { background: linear-gradient(90deg, var(--accent), var(--cyan)) !important; border-radius: 10px !important; }
.stProgress > div { background: var(--card) !important; border-radius: 10px !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

.stNumberInput input { background: var(--card) !important; border-color: var(--border) !important; color: var(--text) !important; border-radius: 12px !important; }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────────
defaults = {
    "score": 0, "total_q": 0, "sessions": 0,
    "chat_history": [], "weak_topics": [],
    "quiz_questions": [], "quiz_answers": {},
    "quiz_submitted": False, "quiz_topic": "",
    "flashcards": [], "study_plan": None,
    "pomodoro_running": False, "pomodoro_start": None,
    "score_history": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────
def parse_json(raw):
    raw = raw.strip()
    if "```" in raw:
        parts = raw.split("```")
        for p in parts:
            p = p.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            if p.startswith(("[","{")):
                raw = p
                break
    return json.loads(raw)

def badge(text, color="#6366f1"):
    return f"<span style='background:{color}22;color:{color};border:1px solid {color}44;padding:0.2rem 0.7rem;border-radius:20px;font-size:11px;font-weight:700;display:inline-block;margin:0.15rem;letter-spacing:0.3px'>{text}</span>"

def glow_card(title, value, icon, color):
    return f"""<div style='background:linear-gradient(135deg,{color}15,{color}08);border:1px solid {color}40;border-radius:16px;padding:1.2rem;text-align:center;'>
        <div style='font-size:1.8rem'>{icon}</div>
        <div style='font-size:1.8rem;font-weight:800;color:{color};margin:0.3rem 0'>{value}</div>
        <div style='color:#64748b;font-size:12px;font-weight:600;letter-spacing:0.5px'>{title}</div>
    </div>"""

def chat_bubble(role, content):
    if role == "user":
        return f"""<div style='display:flex;justify-content:flex-end;margin:0.8rem 0'>
            <div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:18px 18px 4px 18px;padding:0.9rem 1.3rem;max-width:72%;color:white;font-size:14px;line-height:1.7;box-shadow:0 4px 15px rgba(99,102,241,0.3)'>{content}</div>
        </div>"""
    else:
        return f"""<div style='display:flex;justify-content:flex-start;margin:0.8rem 0;gap:0.7rem'>
            <div style='width:32px;height:32px;background:linear-gradient(135deg,#6366f1,#22d3ee);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;margin-top:4px'>🤖</div>
            <div style='background:#12122a;border:1px solid #1e1e4a;border-radius:4px 18px 18px 18px;padding:0.9rem 1.3rem;max-width:75%;color:#e2e8f0;font-size:14px;line-height:1.8;'>{content.replace(chr(10),"<br>")}</div>
        </div>"""

# ── AI FUNCTIONS ──────────────────────────────────────────────────────
def chat_with_bot(question, subject, difficulty, history):
    messages = [{"role": "system", "content": f"""You are EduBot, a world-class AI exam tutor for {subject} at {difficulty} level.
- Give clear structured answers with examples
- Use emojis to make it engaging
- Format with sections for complex topics
- Be encouraging and motivating"""}]
    for h in history[-8:]:
        messages.append(h)
    messages.append({"role": "user", "content": question})
    r = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages, max_tokens=1200)
    return r.choices[0].message.content

def gen_quiz(topic, subject, n, difficulty):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are an expert MCQ creator for {subject}. Return ONLY valid JSON array."},
            {"role": "user", "content": f"""Create {n} MCQ questions on '{topic}' at {difficulty} level.
Return ONLY this JSON array:
[{{"question":"...","options":{{"A":"...","B":"...","C":"...","D":"..."}},"answer":"A","explanation":"..."}}]"""}
        ], max_tokens=2500)
    return r.choices[0].message.content

def gen_flashcards(topic, subject, n):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are a study assistant for {subject}. Return ONLY valid JSON."},
            {"role": "user", "content": f"""Create {n} flashcards on '{topic}'.
Return ONLY this JSON array:
[{{"front":"...","back":"...","category":"...","difficulty":"Easy"}}]"""}
        ], max_tokens=2000)
    return r.choices[0].message.content

def gen_study_plan(subject, days, weak, exam_type, hours):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert academic planner. Return ONLY valid JSON."},
            {"role": "user", "content": f"""Create a {days}-day study plan for {subject} {exam_type} exam. {hours} hours/day. {"Weak topics: "+weak if weak else ""}
Return ONLY this JSON:
{{"overview":"...","daily_goals":[{{"day":1,"topic":"...","subtopics":["..."],"duration":"...","priority":"High","tip":"..."}}],"exam_tips":["..."],"do_not":["..."]}}"""}
        ], max_tokens=3500)
    return r.choices[0].message.content

def gen_formula_sheet(subject, topic):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are an expert in {subject}."},
            {"role": "user", "content": f"Create a comprehensive formula/concept sheet for '{topic}' in {subject}. Include all formulas, definitions, key concepts, units, common mistakes. Format beautifully with clear sections and emojis."}
        ], max_tokens=2000)
    return r.choices[0].message.content

def analyze_answer(question, user_answer, subject):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are a strict but encouraging {subject} examiner."},
            {"role": "user", "content": f"Evaluate this answer and give marks out of 10:\nQuestion: {question}\nStudent Answer: {user_answer}\nGive: Score/10, What was good, What was missing, Model answer, Tips to improve."}
        ], max_tokens=800)
    return r.choices[0].message.content

def process_notes(notes, action, subject):
    prompts = {
        "📋 Summarize": f"Summarize these {subject} notes in clear bullet points:\n\n{notes}",
        "❓ Generate Questions": f"Generate 8 exam questions with answers from these {subject} notes:\n\n{notes}",
        "💡 Explain Concepts": f"Explain all difficult concepts in these {subject} notes with simple examples:\n\n{notes}",
        "🔑 Key Points": f"Extract all key points, formulas, definitions from these {subject} notes:\n\n{notes}",
        "🔗 Mind Map": f"Create a text-based mind map from these {subject} notes:\n\n{notes}",
        "📝 Short Notes": f"Convert these {subject} notes into concise revision notes:\n\n{notes}"
    }
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are an expert {subject} tutor and study coach."},
            {"role": "user", "content": prompts.get(action, notes)}
        ], max_tokens=1500)
    return r.choices[0].message.content

# ── SUBJECTS ──────────────────────────────────────────────────────────
SUBJECTS = [
    "── Science ──","Physics","Chemistry","Biology","Environmental Science","Biotechnology",
    "── Mathematics ──","Mathematics","Statistics","Engineering Mathematics",
    "── Computer Science ──","Computer Science","Data Structures & Algorithms",
    "Database Management","Operating Systems","Computer Networks",
    "Artificial Intelligence","Machine Learning","Web Development",
    "── Commerce ──","Accountancy","Business Studies","Economics",
    "── Humanities ──","History","Geography","Political Science","Psychology","Sociology","Philosophy",
    "── Languages ──","English Literature","Hindi","English Grammar",
    "── Engineering ──","Engineering Drawing","Mechanics","Thermodynamics","Electronics","Circuit Theory",
    "── Other ──","Law","Medical","Custom (type below)"
]

# ── SIDEBAR ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.5rem 0 1rem'>
        <div style='width:64px;height:64px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 0.8rem'>🎓</div>
        <div style='font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#6366f1,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>EduBot AI</div>
        <div style='font-size:11px;color:#64748b;margin-top:0.2rem;letter-spacing:0.5px'>SMART EXAM PREP</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:0.5rem'>📚 SUBJECT</div>", unsafe_allow_html=True)
    subject_choice = st.selectbox("", SUBJECTS, label_visibility="collapsed")
    if subject_choice.startswith("──") or subject_choice == "Custom (type below)":
        subject = st.text_input("", placeholder="Type your subject...", label_visibility="collapsed")
        if not subject:
            subject = "General"
    else:
        subject = subject_choice

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:0.5rem'>⚡ DIFFICULTY</div>", unsafe_allow_html=True)
    difficulty = st.select_slider("", options=["Easy","Medium","Hard","Expert"], value="Medium", label_visibility="collapsed")
    diff_colors = {"Easy":"#10b981","Medium":"#f59e0b","Hard":"#ef4444","Expert":"#8b5cf6"}
    diff_color = diff_colors[difficulty]
    st.markdown(f"<div style='background:{diff_color}22;border:1px solid {diff_color}44;border-radius:8px;padding:0.4rem;text-align:center;color:{diff_color};font-size:12px;font-weight:700'>{difficulty} Mode Active</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:0.8rem'>📊 YOUR STATS</div>", unsafe_allow_html=True)
    acc = int(st.session_state.score / st.session_state.total_q * 100) if st.session_state.total_q > 0 else 0

    c1,c2 = st.columns(2)
    with c1: st.markdown(glow_card("CORRECT", st.session_state.score, "✅", "#10b981"), unsafe_allow_html=True)
    with c2: st.markdown(glow_card("ACCURACY", f"{acc}%", "🎯", "#6366f1"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: st.markdown(glow_card("ATTEMPTED", st.session_state.total_q, "📝", "#f59e0b"), unsafe_allow_html=True)
    with c4: st.markdown(glow_card("SESSIONS", st.session_state.sessions, "🔥", "#ec4899"), unsafe_allow_html=True)

    if st.session_state.total_q > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(acc/100)
        st.markdown(f"<div style='color:#64748b;font-size:11px;text-align:center'>{acc}% Overall Accuracy</div>", unsafe_allow_html=True)

    if st.session_state.weak_topics:
        st.divider()
        st.markdown("<div style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:0.5rem'>⚠️ WEAK TOPICS</div>", unsafe_allow_html=True)
        for t in list(set(st.session_state.weak_topics))[-4:]:
            st.markdown(badge(f"⚡ {t}", "#ef4444"), unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:0.5rem'>⏱️ STUDY TIMER</div>", unsafe_allow_html=True)
    pomo_mins = st.number_input("Minutes", min_value=5, max_value=90, value=25, step=5, label_visibility="collapsed")

    if not st.session_state.pomodoro_running:
        if st.button("▶ Start Timer", use_container_width=True):
            st.session_state.pomodoro_running = True
            st.session_state.pomodoro_start = time.time()
            st.session_state.sessions += 1
            st.rerun()
    else:
        elapsed = int(time.time() - st.session_state.pomodoro_start)
        total = pomo_mins * 60
        remaining = max(0, total - elapsed)
        mins, secs = divmod(remaining, 60)
        st.progress(min(1.0, elapsed/total))
        st.markdown(f"<div style='color:#22d3ee;font-size:1.5rem;font-weight:800;text-align:center;font-family:JetBrains Mono,monospace'>{mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
        if remaining == 0:
            st.success("🎉 Session complete!")
            st.session_state.pomodoro_running = False
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state.pomodoro_running = False
            st.rerun()

    st.divider()
    if st.button("🔄 Reset All Stats", use_container_width=True):
        for k,v in defaults.items(): st.session_state[k] = v
        st.rerun()

    st.markdown("<div style='text-align:center;color:#1e1e4a;font-size:11px;margin-top:1rem'>Made with ❤️ by Harshita<br>INT428 — AI Essentials 2026</div>", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg,#6366f122,#8b5cf611,#22d3ee0a);border:1px solid #1e1e4a;border-radius:20px;padding:2rem 2.5rem;margin-bottom:1.5rem;'>
    <div style='display:flex;align-items:center;gap:1.5rem;'>
        <div style='width:60px;height:60px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 8px 24px rgba(99,102,241,0.4);flex-shrink:0'>🎓</div>
        <div>
            <div style='font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#e2e8f0,#94a3b8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2'>
                EduBot <span style='background:linear-gradient(135deg,#6366f1,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>AI</span>
            </div>
            <div style='color:#64748b;font-size:14px;margin-top:0.3rem'>Studying <strong style='color:#6366f1'>{subject}</strong> · <strong style='color:{diff_color}'>{difficulty}</strong> Mode</div>
        </div>
        <div style='margin-left:auto;display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:flex-end'>
            {badge("🤖 LLaMA 3","#6366f1")}{badge("⚡ Groq API","#8b5cf6")}{badge("🐍 Python","#10b981")}{badge("🌐 Streamlit","#f59e0b")}
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "💬 AI Tutor","📝 Quiz","🃏 Flashcards",
    "📅 Study Plan","📖 Notes AI","🔬 Answer Checker","📐 Formula Sheet"
])

# ════════════════════════ TAB 1 — AI TUTOR ════════════════════════════
with t1:
    st.markdown(f"""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>💬</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>AI Tutor</div>
        <div style='font-size:12px;color:#64748b'>Remembers your conversation · {subject} Expert</div></div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown(f"""<div style='text-align:center;padding:3rem 1rem;'>
            <div style='font-size:3rem;margin-bottom:1rem'>🤖</div>
            <div style='font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:0.5rem'>Hello! I'm EduBot</div>
            <div style='color:#64748b;font-size:14px'>Your AI tutor for {subject}. Ask me anything!</div>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            st.markdown(chat_bubble(msg["role"], msg["content"]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    suggestions_map = {
        "Physics":["Explain Newton's 3 Laws","What is Ohm's Law?","Explain thermodynamics","What is quantum mechanics?"],
        "Chemistry":["What are ionic bonds?","Explain organic reactions","What is pH?","Explain periodic trends"],
        "Mathematics":["Explain integration","What are matrices?","How to solve quadratics?","Explain probability"],
        "Biology":["Explain photosynthesis","What is DNA replication?","Explain cell division","What is homeostasis?"],
        "Computer Science":["What is OOP?","Explain recursion","What are data structures?","Explain Big O notation"],
        "History":["Major causes of WW1","Explain the Cold War","What was colonialism?","Industrial Revolution effects"],
        "Economics":["What is GDP?","Explain inflation","What is supply and demand?","Explain monetary policy"],
        "Artificial Intelligence":["What is machine learning?","Explain neural networks","What is NLP?","Explain reinforcement learning"],
    }
    sugs = suggestions_map.get(subject, ["Explain key concepts","Give me important topics","What should I study first?","Give me exam tips"])

    st.markdown("<div style='color:#64748b;font-size:12px;font-weight:600;margin-bottom:0.5rem'>💡 Quick Questions:</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(col,s) in enumerate(zip(cols,sugs)):
        with col:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                with st.spinner("🤔 Thinking..."):
                    ans = chat_with_bot(s, subject, difficulty, st.session_state.chat_history)
                st.session_state.chat_history += [{"role":"user","content":s},{"role":"assistant","content":ans}]
                st.rerun()

    c1,c2,c3 = st.columns([5,1,1])
    with c1:
        user_q = st.text_input("", placeholder=f"Ask anything about {subject}...", key="chat_q", label_visibility="collapsed")
    with c2:
        send = st.button("Send 🚀", use_container_width=True, key="send_chat")
    with c3:
        if st.button("Clear 🗑️", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    if send and user_q:
        with st.spinner("🤔 Thinking..."):
            ans = chat_with_bot(user_q, subject, difficulty, st.session_state.chat_history)
        st.session_state.chat_history += [{"role":"user","content":user_q},{"role":"assistant","content":ans}]
        st.rerun()

# ════════════════════════ TAB 2 — QUIZ ════════════════════════════════
with t2:
    st.markdown("""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>📝</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>Interactive Quiz</div>
        <div style='font-size:12px;color:#64748b'>Click options · Instant results · Score tracking</div></div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([3,1,1])
    with c1: qtopic = st.text_input("📌 Quiz Topic", placeholder="e.g. Newton's Laws, Sorting Algorithms, Organic Chemistry...")
    with c2: nq = st.selectbox("Questions", [3,5,7,10], index=1)
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        gen_q = st.button("Generate ⚡", use_container_width=True)

    if gen_q and qtopic:
        with st.spinner(f"🎯 Generating {nq} {difficulty} questions..."):
            raw = gen_quiz(qtopic, subject, nq, difficulty)
        try:
            qs = parse_json(raw)
            st.session_state.quiz_questions = qs
            st.session_state.quiz_topic = qtopic
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
        except:
            st.error("⚠️ Could not generate quiz. Try a more specific topic.")

    if st.session_state.quiz_questions:
        qs = st.session_state.quiz_questions
        st.markdown(f"""<div style='background:linear-gradient(135deg,#f59e0b15,#ef444415);border:1px solid #f59e0b33;border-radius:14px;padding:1rem 1.5rem;margin:1rem 0;display:flex;align-items:center;gap:1rem'>
            <div style='font-size:1.5rem'>📚</div>
            <div><div style='color:#f59e0b;font-weight:700;font-size:15px'>{st.session_state.quiz_topic} · {len(qs)} Questions</div>
            <div style='color:#64748b;font-size:12px'>{subject} · {difficulty} Difficulty</div></div>
        </div>""", unsafe_allow_html=True)

        for i,q in enumerate(qs):
            st.markdown(f"""<div style='background:#12122a;border:1px solid #1e1e4a;border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0;'>
                <div style='display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:1rem'>
                    <div style='width:28px;height:28px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:13px;flex-shrink:0'>Q{i+1}</div>
                    <div style='color:#e2e8f0;font-size:15px;font-weight:600;line-height:1.5'>{q['question']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            sel = st.radio("", list(q["options"].keys()),
                format_func=lambda x,q=q: f"  {x})  {q['options'][x]}",
                key=f"q_{i}", horizontal=False, label_visibility="collapsed")
            st.session_state.quiz_answers[i] = sel
            st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✅ Submit Quiz & See Results", use_container_width=True):
            st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            correct = sum(1 for i,q in enumerate(qs) if st.session_state.quiz_answers.get(i)==q["answer"])
            pct = int(correct/len(qs)*100)

            st.markdown("<br><div style='font-size:1.3rem;font-weight:800;color:#e2e8f0;margin-bottom:1rem'>📊 Results</div>", unsafe_allow_html=True)

            for i,q in enumerate(qs):
                ua = st.session_state.quiz_answers.get(i,"")
                ca = q["answer"]
                ok = ua==ca
                bc = "#10b981" if ok else "#ef4444"
                st.markdown(f"""<div style='background:{"#10b98108" if ok else "#ef444408"};border:1px solid {bc}33;border-left:4px solid {bc};border-radius:0 14px 14px 0;padding:1.2rem;margin:0.7rem 0'>
                    <div style='color:{bc};font-weight:700;margin-bottom:0.5rem'>{"✅ Correct!" if ok else "❌ Wrong"} — Q{i+1}</div>
                    <div style='color:#94a3b8;font-size:13px;margin-bottom:0.8rem'>{q["question"]}</div>
                    {"" if ok else f'<div style="color:#ef4444;font-size:13px;margin-bottom:0.3rem">Your answer: {ua}) {q["options"].get(ua,"")}</div>'}
                    <div style='color:#10b981;font-size:13px;margin-bottom:0.5rem'>✅ Correct: {ca}) {q["options"].get(ca,"")}</div>
                    <div style='background:#0d0d1f;border-radius:8px;padding:0.7rem;color:#94a3b8;font-size:12px;line-height:1.6'>📖 <strong style="color:#6366f1">Explanation:</strong> {q.get("explanation","")}</div>
                </div>""", unsafe_allow_html=True)
                if not ok and st.session_state.quiz_topic not in st.session_state.weak_topics:
                    st.session_state.weak_topics.append(st.session_state.quiz_topic)

            medal = "🥇" if pct>=90 else "🥈" if pct>=70 else "🥉" if pct>=50 else "📖"
            sc = "#10b981" if pct>=70 else "#f59e0b" if pct>=50 else "#ef4444"
            msg = "Outstanding! 🌟 Exam ready!" if pct>=90 else "Great job! 💪" if pct>=70 else "Keep practicing! 📚" if pct>=50 else "Review & retry! 🚀"

            st.markdown(f"""<div style='background:linear-gradient(135deg,{sc}15,{sc}08);border:2px solid {sc};border-radius:20px;padding:2.5rem;text-align:center;margin:1.5rem 0'>
                <div style='font-size:3rem;margin-bottom:0.8rem'>{medal}</div>
                <div style='font-size:2.5rem;font-weight:800;color:{sc}'>{correct}/{len(qs)}</div>
                <div style='font-size:1.2rem;color:#94a3b8;margin:0.3rem 0'>{pct}% Score</div>
                <div style='color:#64748b;font-size:14px;margin-top:0.5rem'>{msg}</div>
            </div>""", unsafe_allow_html=True)

            st.session_state.score += correct
            st.session_state.total_q += len(qs)
            st.session_state.score_history.append({"topic":st.session_state.quiz_topic,"score":pct})
            st.session_state.quiz_submitted = False
            st.session_state.quiz_questions = []

# ════════════════════════ TAB 3 — FLASHCARDS ══════════════════════════
with t3:
    st.markdown("""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#ec4899,#8b5cf6);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>🃏</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>Smart Flashcards</div>
        <div style='font-size:12px;color:#64748b'>Visual cards with difficulty ratings</div></div>
    </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns([3,1])
    with c1: fc_topic = st.text_input("📌 Flashcard Topic", placeholder="e.g. Organic Chemistry, Binary Trees, French Revolution...")
    with c2: nc = st.selectbox("Cards", [5,8,10,15,20], index=1)

    if st.button("Generate Flashcards 🃏", use_container_width=True):
        if fc_topic:
            with st.spinner("🃏 Creating your flashcards..."):
                raw = gen_flashcards(fc_topic, subject, nc)
            try:
                cards = parse_json(raw)
                st.session_state.flashcards = cards
            except:
                st.error("Could not generate. Try a different topic.")

    if st.session_state.flashcards:
        cards = st.session_state.flashcards
        filter_diff = st.radio("Filter by difficulty:", ["All","Easy","Medium","Hard"], horizontal=True)
        filtered = cards if filter_diff=="All" else [c for c in cards if c.get("difficulty")==filter_diff]

        diff_colors_map = {"Easy":"#10b981","Medium":"#f59e0b","Hard":"#ef4444"}
        cols = st.columns(2)
        for i,card_data in enumerate(filtered):
            dc = diff_colors_map.get(card_data.get("difficulty","Medium"),"#6366f1")
            with cols[i%2]:
                st.markdown(f"""<div style='background:linear-gradient(135deg,#12122a,#16163a);border:1px solid {dc}44;border-radius:16px;padding:1.4rem;margin:0.6rem 0;'>
                    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem'>
                        <span style='color:#475569;font-size:11px;font-weight:700'>CARD {i+1}</span>
                        <span style='background:{dc}22;color:{dc};padding:0.15rem 0.6rem;border-radius:10px;font-size:10px;font-weight:700'>{card_data.get("difficulty","")}</span>
                    </div>
                    <div style='color:#6366f1;font-weight:700;font-size:14px;margin-bottom:0.8rem;line-height:1.5'>❓ {card_data.get("front","")}</div>
                    <div style='height:1px;background:linear-gradient(90deg,transparent,{dc}44,transparent);margin:0.8rem 0'></div>
                    <div style='color:#94a3b8;font-size:13px;line-height:1.7'>💡 {card_data.get("back","")}</div>
                    {f'<div style="margin-top:0.8rem"><span style="background:#6366f122;color:#6366f1;padding:0.15rem 0.6rem;border-radius:8px;font-size:10px">📂 {card_data.get("category","")}</span></div>' if card_data.get("category") else ""}
                </div>""", unsafe_allow_html=True)

# ════════════════════════ TAB 4 — STUDY PLAN ══════════════════════════
with t4:
    st.markdown("""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#10b981,#22d3ee);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>📅</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>Smart Study Planner</div>
        <div style='font-size:12px;color:#64748b'>Personalized day-by-day exam plan</div></div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: days = st.slider("📆 Days to Exam", 1, 60, 7)
    with c2: exam_type = st.selectbox("🎯 Exam Type", ["University Final","Mid-term","Board Exam","Competitive","Entrance","Weekly Test"])
    with c3: hours = st.slider("⏰ Hours/Day", 1, 12, 4)
    weak = st.text_input("⚠️ Weak Topics", placeholder="e.g. integration, Newton's laws, organic chemistry...")

    if st.button("🚀 Generate My Study Plan", use_container_width=True):
        with st.spinner("📅 Building your personalized plan..."):
            raw = gen_study_plan(subject, days, weak, exam_type, hours)
        try:
            plan = parse_json(raw)
            st.session_state.study_plan = plan
        except:
            st.error("Could not generate. Please try again.")

    if st.session_state.study_plan:
        plan = st.session_state.study_plan
        st.markdown(f"""<div style='background:linear-gradient(135deg,#10b98115,#22d3ee08);border:1px solid #10b98133;border-radius:16px;padding:1.5rem;margin:1rem 0'>
            <div style='color:#10b981;font-weight:700;font-size:15px;margin-bottom:0.5rem'>📋 Study Strategy</div>
            <div style='color:#e2e8f0;line-height:1.7;font-size:14px'>{plan.get("overview","")}</div>
        </div>""", unsafe_allow_html=True)

        priority_colors = {"High":"#ef4444","Medium":"#f59e0b","Low":"#10b981"}
        for day in plan.get("daily_goals",[]):
            pc = priority_colors.get(day.get("priority","Medium"),"#6366f1")
            with st.expander(f"📌 Day {day['day']} — {day.get('topic','')}  |  ⏱️ {day.get('duration','')}  |  🎯 {day.get('priority','')} Priority", expanded=day.get("day",99)<=3):
                dc1,dc2 = st.columns([2,1])
                with dc1:
                    st.markdown("<div style='font-weight:700;color:#e2e8f0;margin-bottom:0.7rem'>📚 Tasks:</div>", unsafe_allow_html=True)
                    for task in day.get("subtopics",day.get("tasks",[])):
                        st.markdown(f"<div style='display:flex;align-items:flex-start;gap:0.5rem;margin:0.3rem 0;color:#94a3b8;font-size:13px'><span style='color:#10b981;flex-shrink:0'>✅</span>{task}</div>", unsafe_allow_html=True)
                with dc2:
                    st.markdown(f"""<div style='background:{pc}11;border:1px solid {pc}33;border-radius:12px;padding:1rem;text-align:center'>
                        <div style='color:{pc};font-size:11px;font-weight:700;letter-spacing:0.5px'>{day.get("priority","").upper()} PRIORITY</div>
                        <div style='height:1px;background:{pc}33;margin:0.7rem 0'></div>
                        <div style='color:#22d3ee;font-size:11px;font-weight:700;margin-bottom:0.4rem'>💡 TIP</div>
                        <div style='color:#94a3b8;font-size:12px;line-height:1.6'>{day.get("tip","")}</div>
                    </div>""", unsafe_allow_html=True)

        if plan.get("exam_tips"):
            st.markdown("<div style='font-size:1rem;font-weight:700;color:#e2e8f0;margin:1.5rem 0 0.8rem'>🏆 Exam Day Tips</div>", unsafe_allow_html=True)
            for i,tip in enumerate(plan["exam_tips"],1):
                st.markdown(f"""<div style='background:#f59e0b0a;border-left:3px solid #f59e0b;border-radius:0 10px 10px 0;padding:0.8rem 1rem;margin:0.4rem 0;color:#e2e8f0;font-size:14px'>
                    <strong style='color:#f59e0b'>Tip {i}:</strong> {tip}</div>""", unsafe_allow_html=True)

        if plan.get("do_not"):
            st.markdown("<div style='font-size:1rem;font-weight:700;color:#e2e8f0;margin:1.5rem 0 0.8rem'>🚫 What NOT To Do</div>", unsafe_allow_html=True)
            for don in plan["do_not"]:
                st.markdown(f"""<div style='background:#ef44440a;border-left:3px solid #ef4444;border-radius:0 10px 10px 0;padding:0.7rem 1rem;margin:0.4rem 0;color:#94a3b8;font-size:13px'>
                    <span style='color:#ef4444'>❌</span> {don}</div>""", unsafe_allow_html=True)

# ════════════════════════ TAB 5 — NOTES AI ════════════════════════════
with t5:
    st.markdown("""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#22d3ee,#6366f1);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>📖</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>Notes AI</div>
        <div style='font-size:12px;color:#64748b'>Paste your notes · Get summaries, questions, key points</div></div>
    </div>""", unsafe_allow_html=True)

    notes = st.text_area("📝 Paste your notes here", height=220, placeholder="Paste your notes, textbook content or any study material here...")
    action = st.radio("🎯 What do you want?", ["📋 Summarize","❓ Generate Questions","💡 Explain Concepts","🔑 Key Points","🔗 Mind Map","📝 Short Notes"], horizontal=True)

    if st.button("Process Notes 🚀", use_container_width=True):
        if notes.strip():
            with st.spinner("🔍 Processing your notes..."):
                result = process_notes(notes, action, subject)
            st.markdown(f"""<div style='background:#12122a;border:1px solid #1e1e4a;border-radius:16px;padding:1.5rem;margin:1rem 0;'>
                <div style='color:#6366f1;font-weight:700;font-size:14px;margin-bottom:1rem'>{action} Results</div>
                <div style='color:#e2e8f0;font-size:14px;line-height:1.8;white-space:pre-wrap'>{result}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please paste your notes first!")

# ════════════════════════ TAB 6 — ANSWER CHECKER ══════════════════════
with t6:
    st.markdown("""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#ec4899);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>🔬</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>Answer Checker</div>
        <div style='font-size:12px;color:#64748b'>Write your answer · Get marks + detailed feedback</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div style='background:#f59e0b0a;border:1px solid #f59e0b33;border-radius:12px;padding:1rem;margin-bottom:1rem;color:#94a3b8;font-size:13px'>
        💡 Write your answer to any question and I will grade it like a teacher — marks out of 10, feedback, and a model answer!
    </div>""", unsafe_allow_html=True)

    aq = st.text_area("❓ Question", height=80, placeholder="Paste the exam question here...")
    aa = st.text_area("✍️ Your Answer", height=200, placeholder="Write your answer as you would in an exam...")

    if st.button("📊 Evaluate My Answer", use_container_width=True):
        if aq and aa:
            with st.spinner("🔬 Evaluating your answer..."):
                feedback = analyze_answer(aq, aa, subject)
            st.markdown(f"""<div style='background:#12122a;border:1px solid #6366f133;border-radius:16px;padding:1.5rem;margin:1rem 0'>
                <div style='color:#6366f1;font-weight:700;font-size:14px;margin-bottom:1rem'>📊 Teacher Feedback</div>
                <div style='color:#e2e8f0;font-size:14px;line-height:1.9;white-space:pre-wrap'>{feedback}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please enter both question and your answer!")

# ════════════════════════ TAB 7 — FORMULA SHEET ═══════════════════════
with t7:
    st.markdown("""<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
        <div style='width:40px;height:40px;background:linear-gradient(135deg,#8b5cf6,#ec4899);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px'>📐</div>
        <div><div style='font-size:1.1rem;font-weight:700;color:#e2e8f0'>Formula & Concept Sheet</div>
        <div style='font-size:12px;color:#64748b'>Instant formula sheets for any topic</div></div>
    </div>""", unsafe_allow_html=True)

    ft = st.text_input("📌 Topic", placeholder="e.g. Thermodynamics, Integration, Organic Chemistry, Sorting Algorithms...")

    if st.button("📐 Generate Formula Sheet", use_container_width=True):
        if ft:
            with st.spinner("📐 Building your formula sheet..."):
                fs = gen_formula_sheet(subject, ft)
            st.markdown(f"""<div style='background:#12122a;border:1px solid #8b5cf633;border-radius:16px;padding:1.5rem;margin:1rem 0;'>
                <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem'>
                    <div style='width:32px;height:32px;background:linear-gradient(135deg,#8b5cf6,#ec4899);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px'>📐</div>
                    <div style='color:#8b5cf6;font-weight:700;font-size:15px'>{ft} — {subject} Formula Sheet</div>
                </div>
                <div style='color:#e2e8f0;font-size:14px;line-height:1.9;white-space:pre-wrap'>{fs}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please enter a topic!")
