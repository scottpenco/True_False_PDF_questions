import streamlit as st
import fitz  # PyMuPDF
import openai
import random

# Set OpenAI API Key
openai.api_key = "your-api-key"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(streamlit_uploaded_file=pdf_file)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# Function to generate true/false questions
def generate_tf_questions(text):
    prompt = f"Extract key facts from the following text and convert them into true/false questions:\n{text[:2000]}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    questions = response["choices"][0]["message"]["content"].split("\n")
    tf_questions = []
    
    for q in questions:
        if q.strip().endswith("?"):
            answer = random.choice(["True", "False"])
            tf_questions.append({"question": q.strip(), "answer": answer})

    return tf_questions

# Streamlit UI
st.title("PDF Academic Paper - True/False Quiz Generator")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    st.write("Extracting text and generating questions...")
    extracted_text = extract_text_from_pdf(uploaded_file)
    
    if extracted_text:
        questions = generate_tf_questions(extracted_text)
        st.session_state["questions"] = questions
        st.session_state["current_index"] = 0
        st.session_state["score"] = 0
    else:
        st.error("Could not extract text. Try another PDF.")

# Display Questions
if "questions" in st.session_state and st.session_state["questions"]:
    index = st.session_state["current_index"]
    question = st.session_state["questions"][index]

    st.subheader(f"Question {index+1}")
    st.write(question["question"])

    user_answer = st.radio("Your Answer:", ["True", "False"])

    if st.button("Submit Answer"):
        correct = user_answer == question["answer"]
        if correct:
            st.success("Correct!")
            st.session_state["score"] += 1
        else:
            st.error(f"Incorrect! The correct answer is {question['answer']}.")

        if index + 1 < len(st.session_state["questions"]):
            st.session_state["current_index"] += 1
        else:
            st.write(f"Quiz Complete! Your Score: {st.session_state['score']} / {len(st.session_state['questions'])}")
            st.session_state.pop("questions")
            st.session_state.pop("current_index")
            st.session_state.pop("score")
