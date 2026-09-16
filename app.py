import os
import streamlit as st

API_KEY = "AQ.Ab8RN6LuXrV4HbVtBmxH1WqEERysbl4FKLmSSiFWP4DPvcLd_w"
os.environ["GOOGLE_API_KEY"] = API_KEY

from google import genai
from google.genai import types
from audiorecorder import audiorecorder

# Page Configuration
st.set_page_config(page_title="My AI English & IELTS Teacher", page_icon="🎓", layout="wide")

st.title("🎓 My Personal AI English & IELTS Teacher")
st.write("Record your voice directly in the browser or type out whatever is on your mind. The AI will instantly evaluate your level, score, mistakes, and provide the correct answers.")

# Initialize Gemini Client normally with the AI Studio key
client = genai.Client(api_key=API_KEY)

# Tabs for Speaking and Writing Practice
tab1, tab2 = st.tabs(["🎤 Speaking Practice (Record & Evaluate)", "✍️ Writing & Typing Practice (Type & Evaluate)"])

# --- TAB 1: SPEAKING PRACTICE ---
with tab1:
    st.subheader("Check Your Speaking Skills")
    st.markdown("Click the **Record** button below to start speaking, and click it again to stop recording:")

    audio = audiorecorder("Click to Record", "Recording... Click to Stop")

    if len(audio) > 0:
        st.audio(audio.export().read())
        
        if st.button("Evaluate My Speaking"):
            with st.spinner("AI is analyzing your speech..."):
                try:
                    audio_bytes_io = audio.export(format="wav")
                    audio_bytes = audio_bytes_io.read()

                    prompt_speaking = """
                    You are a friendly and helpful IELTS Speaking Examiner and English Teacher. 
                    Listen to this audio recording carefully and provide feedback in a very clear, simple structure:
                    1. **Estimated Score / Level:** (e.g., Band 5.5, Band 6.0, or Beginner/Intermediate level)
                    2. **What You Said (Summary):**
                    3. **Mistakes & Weaknesses:** (Grammar, pronunciation, or phrasing errors)
                    4. **Correct Answers & Better Way to Say It:**
                    5. **Encouragement & Tips:**
                    """

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[
                            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                            prompt_speaking
                        ]
                    )

                    st.success("Evaluation Complete!")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- TAB 2: WRITING PRACTICE ---
with tab2:
    st.subheader("Type Your Thoughts & Sentences (Writing & Typing)")
    st.markdown("Type anything you want in English (essays, thoughts, stories, sentences) in the box below:")

    user_text = st.text_area("Type your English here:", height=200, placeholder="Type your English sentences or thoughts here...")

    if st.button("Evaluate My Writing"):
        if not user_text.strip():
            st.warning("Please type something before evaluating.")
        else:
            with st.spinner("AI is analyzing your writing..."):
                try:
                    prompt_writing = f"""
                    You are an expert English and IELTS Teacher. 
                    Analyze the following text written by a student:
                    '{user_text}'
                    
                    Please provide the response in a very clear, encouraging, and detailed structure:
                    1. **Estimated Score / Level:** (e.g., IELTS Band 6.0 or CEFR Level)
                    2. **Mistakes Found:** (Grammar, spelling, or structural errors)
                    3. **Corrected Version / Right Answers:**
                    4. **Simple Vocabulary & Tips to Improve:**
                    """

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_writing,
                    )

                    st.success("Evaluation Complete!")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
