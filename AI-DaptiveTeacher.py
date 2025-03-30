import streamlit as st
import requests
from textblob import TextBlob

# HelpingAI API details
API_KEY = "hl-aea67ab9-6430-44c1-90e5-c6e2bbff020b"
API_URL = "https://api.helpingai.co/v1/chat/completions"

def analyze_sentiment(text):
    #Analyzes sentiment and categorizes it as Positive, Neutral, or Negative.
    sentiment_score = TextBlob(text).sentiment.polarity
    if sentiment_score > 0.2:
        return "positive"
    elif sentiment_score < -0.2:
        return "negative"
    else:
        return "neutral"

def get_ai_response(user_input, sentiment):
    #Fetches AI response from HelpingAI API based on sentiment and user input.
    teaching_style = {
        "negative": "Explain it in the simplest way possible with encouragement.",
        "positive": "Challenge the student with a more advanced explanation.",
        "neutral": "Provide a balanced, clear explanation."
    }[sentiment]

    # API request
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

# Streamlit UI
st.title("🤖 AI-Daptive Teacher")
st.subheader("A Personalized AI Tutor That Adapts to You! 🎓")

st.markdown("Ask any question, and the AI will **adjust its response** based on your emotions. 😊😕")

# User input
user_input = st.text_area("💬 Enter your question:", "")

if st.button("Get Answer"):
    if user_input.strip():
        sentiment = analyze_sentiment(user_input)
        st.write(f"🔍 **Detected Sentiment:** {sentiment.capitalize()}")

        with st.spinner("Thinking... 💭"):
            ai_response = get_ai_response(user_input, sentiment)

        st.success("Here's your answer:")
        st.write(f"🤖 **AI-Daptive Teacher ({sentiment.capitalize()} Mode):** {ai_response}")
    else:
        st.warning("⚠️ Please enter a question!")

st.markdown("👨‍🏫 *Keep learning, one step at a time!*")


