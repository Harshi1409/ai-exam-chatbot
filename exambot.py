import streamlit as st
from groq import Groq

# ---- Setup ----
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

def ask_exambot(question, subject="General"):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are an expert exam preparation assistant for {subject}. Answer clearly and simply for a student."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def generate_quiz(topic, subject, num_questions=3):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are an exam assistant for {subject}."},
            {"role": "user", "content": f"""Generate {num_questions} MCQ questions on '{topic}'.
Format exactly like this:
Q1. [question]
A) option  B) option  C) option  D) option
Answer: [letter]
Explanation: [reason]
---"""}
        ]
    )
    return response.choices[0].message.content

def generate_flashcards(topic, subject, num_cards=5):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are an exam assistant for {subject}."},
            {"role": "user", "content": f"""Create {num_cards} flashcards for '{topic}'.
Format exactly like this:
🃏 Card 1
FRONT: [concept]
BACK: [explanation]
"""}
        ]
    )
    return response.choices[0].message.content

def generate_study_plan(subject, days=7, weak_topics=""):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a study planner assistant."},
            {"role": "user", "content": f"""Create a {days}-day study plan for {subject} exam.
{"Focus on weak topics: " + weak_topics if weak_topics else ""}
Format:
Day 1: [topic] - [time] - [what to do]
End with 3 exam tips."""}
        ]
    )
    return response.choices[0].message.content

# ---- Website UI ----
st.set_page_config(page_title="AI Exam Prep Bot", page_icon="🎓", layout="centered")

st.title("🎓 AI Exam Preparation Chatbot")
st.caption("Your personal AI study assistant — powered by Groq & LLaMA")

# Subject selector
subject = st.selectbox("📚 Select your subject:", 
    ["Physics", "Chemistry", "Mathematics", "Biology", "History", "Computer Science", "Other"])

# Mode selector
mode = st.radio("Choose mode:", 
    ["💬 Ask a Question", "📝 Generate Quiz", "🃏 Flashcards", "📅 Study Plan"],
    horizontal=True)

st.divider()

# Mode 1 — Ask a question
if mode == "💬 Ask a Question":
    st.subheader("Ask anything about your subject")
    question = st.text_input("Your question:")
    if st.button("Get Answer 🚀"):
        if question:
            with st.spinner("Thinking..."):
                answer = ask_exambot(question, subject)
            st.success("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question!")

# Mode 2 — Quiz
elif mode == "📝 Generate Quiz":
    st.subheader("Quiz Generator")
    topic = st.text_input("Enter topic (e.g. Newton's Laws):")
    num_q = st.slider("Number of questions:", 1, 10, 3)
    if st.button("Generate Quiz 📝"):
        if topic:
            with st.spinner("Creating quiz..."):
                quiz = generate_quiz(topic, subject, num_q)
            st.success("Your Quiz:")
            st.write(quiz)
        else:
            st.warning("Please enter a topic!")

# Mode 3 — Flashcards
elif mode == "🃏 Flashcards":
    st.subheader("Flashcard Generator")
    topic = st.text_input("Enter topic for flashcards:")
    num_cards = st.slider("Number of cards:", 1, 10, 5)
    if st.button("Generate Flashcards 🃏"):
        if topic:
            with st.spinner("Creating flashcards..."):
                cards = generate_flashcards(topic, subject, num_cards)
            st.success("Your Flashcards:")
            st.write(cards)
        else:
            st.warning("Please enter a topic!")

# Mode 4 — Study Plan
elif mode == "📅 Study Plan":
    st.subheader("Personalized Study Plan")
    days = st.slider("Days until exam:", 1, 30, 7)
    weak_topics = st.text_input("Your weak topics (optional, e.g. trigonometry, matrices):")
    if st.button("Generate Study Plan 📅"):
        with st.spinner("Creating your plan..."):
            plan = generate_study_plan(subject, days, weak_topics)
        st.success("Your Study Plan:")
        st.write(plan)

st.divider()
st.caption("Built with Python, Groq API & Streamlit ❤️")