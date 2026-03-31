import streamlit as st
from textblob import TextBlob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="AI Interview App")

st.title("AI Interview Evaluation System")

questions = [
    "Tell me about yourself",
    "What are your strengths?",
    "What are your weaknesses?",
    "Why should we hire you?",
    "Where do you see yourself in 5 years?"
]

if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.answers = []
    st.session_state.scores = []

def analyze_answer(answer):
    blob = TextBlob(answer)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        emotion = "Confident"
        score = 8
        feedback = "Good answer with positive tone."
    elif polarity == 0:
        emotion = "Neutral"
        score = 6
        feedback = "Try to add more confidence."
    else:
        emotion = "Nervous"
        score = 4
        feedback = "Try to be more confident and positive."

    return emotion, score, feedback

if st.session_state.q_index < len(questions):
    st.subheader("Question:")
    st.write(questions[st.session_state.q_index])

    answer = st.text_area("Type your answer (Use Windows + H for voice typing)")

    if st.button("Analyze Answer"):
        emotion, score, feedback = analyze_answer(answer)

        st.write("Emotion:", emotion)
        st.write("Score:", score)
        st.write("Feedback:", feedback)

        st.session_state.answers.append(answer)
        st.session_state.scores.append(score)

    if st.button("Next Question"):
        st.session_state.q_index += 1
        st.rerun()

else:
    st.subheader("Interview Completed")

    total_score = sum(st.session_state.scores)
    st.write("Final Score:", total_score)

    if st.button("Generate Report"):
        c = canvas.Canvas("Interview_Report.pdf", pagesize=letter)
        c.drawString(100, 750, "AI Interview Report")

        y = 700
        for i, ans in enumerate(st.session_state.answers):
            c.drawString(100, y, f"Q{i+1}: {questions[i]}")
            y -= 20
            c.drawString(100, y, f"Answer: {ans}")
            y -= 40

        c.drawString(100, y, f"Final Score: {total_score}")
        c.save()

        st.success("Report Generated: Interview_Report.pdf")
      
