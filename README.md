# 🎓 AI Exam Preparation Chatbot

An AI-powered study assistant that helps students prepare for exams 
using Large Language Models (LLM). Built with Python, Groq API, and Streamlit.


## 📌 Project Overview

This project was built as part of the **Artificial Intelligence Essentials** 
course. The chatbot uses the LLaMA 3 language model via Groq API to help 
students study smarter — not harder.


## ✨ Features

- 💬 **Ask a Question** — Get instant AI-powered answers on any topic
- 📝 **Quiz Generator** — Generate MCQ questions with answers and explanations
- 🃏 **Flashcard Generator** — Create flashcards for quick revision
- 📅 **Study Plan Generator** — Get a personalized day-by-day study plan
- 📚 **Multiple Subjects** — Physics, Chemistry, Math, Biology, CS and more


## 📸 Screenshots

### 💬 Ask a Question
![Home](home.png)

### 📝 Quiz Generator
![Quiz](quiz.png)

### 🃏 Flashcards
![Flashcards](flashcards.png)

### 📅 Study Plan
![Study Plan](studyplan.png)


## 🛠️ Tech Stack

| Technology | Purpose |
| Python | Core programming language |
| Groq API | AI model access |
| LLaMA 3 (llama-3.1-8b-instant) | Large Language Model |
| Streamlit | Web application framework |
| Jupyter Notebook | Development and testing |


## 🚀 How to Run Locally

**Step 1 — Clone the repository**
git clone https://github.com/yourusername/ai-exam-chatbot.git
cd ai-exam-chatbot

**Step 2 — Install dependencies**
pip install groq streamlit

**Step 3 — Add your API key**

Get a free API key from https://console.groq.com
Open exambot.py and replace:
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
with your actual key.

**Step 4 — Run the app**
streamlit run exambot.py

**Step 5 — Open in browser**
http://localhost:8501



## 💡 How It Works

1. User selects a subject and mode on the website
2. The input is sent to Groq API with a carefully crafted prompt
3. LLaMA 3 model processes the request
4. The AI response is displayed on the Streamlit interface

This is called **Prompt Engineering** — designing smart instructions
that tell the AI exactly how to respond.



## 🧠 AI Concepts Used

- **Large Language Models (LLM)** — AI models trained on large amounts of text
- **Prompt Engineering** — Crafting effective instructions for AI models
- **API Integration** — Connecting Python code to external AI services
- **Generative AI** — AI that generates new content like text and answers



## 📁 Project Structure
ai-exam-chatbot/
│
├── exambot.py          # Main Streamlit web application
├── README.md           # Project documentation
├── home.png            # Screenshot - Ask a Question
├── quiz.png            # Screenshot - Quiz Generator
├── flashcards.png      # Screenshot - Flashcards
└── studyplan.png       # Screenshot - Study Plan



## 👩‍💻 About

**Built by:** Harshita  
**Course:** Artificial Intelligence Essentials  
**Year:** 2026



## 📜 License

This project is open source and available for educational purposes.



⭐ If you found this helpful, please give it a star on GitHub!
