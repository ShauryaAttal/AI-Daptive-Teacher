import streamlit as st
import requests
from textblob import TextBlob

# HelpingAI API details
API_KEY = "hl-aea67ab9-6430-44c1-90e5-c6e2bbff020b"
API_URL = "https://api.helpingai.co/v1/chat/completions"

def analyze_sentiment(text):
    """Analyzes sentiment and categorizes it as Positive, Neutral, or Negative."""
    sentiment_score = TextBlob(text).sentiment.polarity
    if sentiment_score > 0.2:
        return "positive"
    elif sentiment_score < -0.2:
        return "negative"
    else:
        return "neutral"

def get_ai_response(user_input, sentiment):
    """Fetches AI response from HelpingAI API based on sentiment and user input."""
    teaching_style = {
        "negative": "Explain it in the simplest way possible with encouragement.",
        "positive": "Challenge the student with a more advanced explanation.",
        "neutral": "Provide a balanced, clear explanation."
    }[sentiment]

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "helpingai2.5-10b",
            "messages": [
                {"role": "system", "content": teaching_style},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠️ Error: Unable to get a response from AI."

# Streamlit UI (ChatGPT-style)
st.title("🤖 AI-Daptive Teacher")
st.markdown("### A Personalized AI Tutor That Adapts to You! 🎓")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Use text_input instead of st.chat_input
user_input = st.text_input("Ask me anything about your studies!", "")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Analyze sentiment
    sentiment = analyze_sentiment(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 💭"):
            ai_response = get_ai_response(user_input, sentiment)
            st.markdown(f"🤖 **({sentiment.capitalize()} Mode)**: {ai_response}")

    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
